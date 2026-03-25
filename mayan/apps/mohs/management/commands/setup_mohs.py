"""
Bootstrap MoHS directorate structure in Mayan EDMS.

Creates per-directorate: Django group, Role, root cabinet, document types,
metadata bindings, and ACLs so staff in each group can use only their unit.

Run after migrate (and optional initialsetup):

    python manage.py setup_mohs
    python manage.py setup_mohs --with-auditor

Safe to run multiple times (idempotent).
"""
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from mayan.apps.acls.models import AccessControlList
from mayan.apps.cabinets.models import Cabinet
from mayan.apps.cabinets.permissions import (
    permission_cabinet_add_document,
    permission_cabinet_remove_document,
    permission_cabinet_view,
)
from mayan.apps.documents.models import DocumentType
from mayan.apps.documents.permissions import (
    permission_document_create,
    permission_document_download,
    permission_document_edit,
    permission_document_new_version,
    permission_document_print,
    permission_document_properties_edit,
    permission_document_trash,
    permission_document_type_view,
    permission_document_version_view,
    permission_document_view,
)
from mayan.apps.metadata.models import DocumentTypeMetadataType, MetadataType
from mayan.apps.metadata.permissions import (
    permission_document_metadata_add,
    permission_document_metadata_edit,
    permission_document_metadata_view,
)
from mayan.apps.permissions.classes import Permission
from mayan.apps.permissions.models import Role

from mayan.apps.mohs.literals import (
    MOHS_DIRECTORATES,
    mohs_record_types_for,
)


def _stored(*permissions):
    return [p.stored_permission for p in permissions]


class Command(BaseCommand):
    help = (
        'Create MoHS directorate groups, roles, cabinets, document types, '
        'metadata, and ACLs (idempotent).'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--with-auditor',
            action='store_true',
            dest='with_auditor',
            help=(
                'Create MoHS_Auditor_ReadOnly group and read-only ACLs on '
                'all MoHS cabinets and document types.'
            ),
        )

    def handle(self, *args, **options):
        Permission.initialize()
        self._validate_record_type_label_lengths()

        with transaction.atomic():
            meta_types = self._ensure_metadata_types()
            for code, cabinet_label, _full_name in MOHS_DIRECTORATES:
                self._ensure_directorate(
                    code=code,
                    cabinet_label=cabinet_label,
                    metadata_types=meta_types,
                )
            if options['with_auditor']:
                self._ensure_auditor_readonly()

        self.stdout.write(
            self.style.SUCCESS(
                'MoHS setup complete for %s directorates (record types are '
                'defined per unit in mayan.apps.mohs.literals). '
                'Assign users to MoHS_<CODE> groups in Django admin.'
                % len(MOHS_DIRECTORATES)
            )
        )
        if options['with_auditor']:
            self.stdout.write(
                self.style.SUCCESS(
                    'Auditor role ready: assign users to group '
                    'MoHS_Auditor_ReadOnly.'
                )
            )

    def _ensure_metadata_types(self):
        specs = (
            (
                'mohs_record_reference',
                'Record / file reference',
                True,
            ),
            (
                'mohs_physical_location',
                'Physical location (shelf, box, room — if applicable)',
                False,
            ),
            (
                'mohs_storage_mode',
                'Storage mode (Digital / Physical / Hybrid)',
                False,
            ),
        )
        result = []
        for name, label, required in specs:
            mt, created = MetadataType.objects.get_or_create(
                name=name,
                defaults={'label': label},
            )
            if not created and mt.label != label:
                mt.label = label
                mt.save()
            result.append((mt, required))
        return result

    def _validate_record_type_label_lengths(self):
        max_label = 96
        for code, _cab, _full in MOHS_DIRECTORATES:
            for category in mohs_record_types_for(code):
                label = '%s – %s' % (code, category)
                if len(label) > max_label:
                    raise CommandError(
                        'Document type label exceeds %s characters (%s): %r'
                        % (max_label, len(label), label)
                    )

    def _ensure_directorate(self, code, cabinet_label, metadata_types):
        group, _ = Group.objects.get_or_create(name='MoHS_%s' % code)
        role_label = 'MoHS %s Staff' % code
        role, role_created = Role.objects.get_or_create(
            label=role_label,
        )
        role.groups.add(group)

        cabinet, _ = Cabinet.objects.get_or_create(
            parent=None,
            label=cabinet_label,
        )

        ct_cabinet = ContentType.objects.get_for_model(Cabinet)

        acl_cabinet, _ = AccessControlList.objects.get_or_create(
            content_type=ct_cabinet,
            object_id=cabinet.pk,
            role=role,
        )
        acl_cabinet.permissions.add(
            *_stored(
                permission_cabinet_view,
                permission_cabinet_add_document,
                permission_cabinet_remove_document,
            )
        )

        for category in mohs_record_types_for(code):
            doc_type_label = '%s – %s' % (code, category)
            document_type, _ = DocumentType.objects.get_or_create(
                label=doc_type_label,
            )
            for mt, required in metadata_types:
                DocumentTypeMetadataType.objects.get_or_create(
                    document_type=document_type,
                    metadata_type=mt,
                    defaults={'required': required},
                )
            self._grant_staff_document_type_acl(role, document_type)

        self.stdout.write(
            '%s %s → group %s, role "%s" (%s document types)' % (
                'Created' if role_created else 'Updated',
                code,
                group.name,
                role_label,
                len(mohs_record_types_for(code)),
            )
        )

    def _grant_staff_document_type_acl(self, role, document_type):
        ct_doctype = ContentType.objects.get_for_model(DocumentType)
        acl_dt, _ = AccessControlList.objects.get_or_create(
            content_type=ct_doctype,
            object_id=document_type.pk,
            role=role,
        )
        acl_dt.permissions.add(
            *_stored(
                permission_document_type_view,
                permission_document_create,
                permission_document_view,
                permission_document_edit,
                permission_document_download,
                permission_document_new_version,
                permission_document_properties_edit,
                permission_document_print,
                permission_document_trash,
                permission_document_metadata_view,
                permission_document_metadata_add,
                permission_document_metadata_edit,
            )
        )

    def _ensure_auditor_readonly(self):
        group, _ = Group.objects.get_or_create(name='MoHS_Auditor_ReadOnly')
        role_label = 'MoHS Auditor (read-only)'
        role, _ = Role.objects.get_or_create(label=role_label)
        role.groups.add(group)

        ct_cabinet = ContentType.objects.get_for_model(Cabinet)
        ct_doctype = ContentType.objects.get_for_model(DocumentType)

        for _code, cabinet_label, _full in MOHS_DIRECTORATES:
            cabinet = Cabinet.objects.filter(
                parent__isnull=True, label=cabinet_label
            ).first()
            if not cabinet:
                continue
            acl, _ = AccessControlList.objects.get_or_create(
                content_type=ct_cabinet,
                object_id=cabinet.pk,
                role=role,
            )
            acl.permissions.add(*_stored(permission_cabinet_view))

        for code, _cab, _full in MOHS_DIRECTORATES:
            for category in mohs_record_types_for(code):
                label = '%s – %s' % (code, category)
                document_type = DocumentType.objects.filter(
                    label=label
                ).first()
                if not document_type:
                    continue
                acl, _ = AccessControlList.objects.get_or_create(
                    content_type=ct_doctype,
                    object_id=document_type.pk,
                    role=role,
                )
                acl.permissions.add(
                    *_stored(
                        permission_document_type_view,
                        permission_document_view,
                        permission_document_version_view,
                        permission_document_download,
                        permission_document_metadata_view,
                    )
                )
