# MoHS — Ministry of Health and Sanitation, Sierra Leone.
#
# Record types below are aligned to typical directorate mandates. When your
# approved Records / Archiving Schedule is issued, replace tuples with the
# exact class names from that policy (each suffix + "CODE – " must stay ≤ 96
# chars — DocumentType.label limit in Mayan).

MOHS_DEFAULT_RECORD_TYPES = ('General records',)


def mohs_record_types_for(directorate_code):
    return MOHS_RECORD_TYPES_BY_DIRECTORATE.get(
        directorate_code, MOHS_DEFAULT_RECORD_TYPES
    )


# Per-directorate record classes (one Mayan document type per string).
MOHS_RECORD_TYPES_BY_DIRECTORATE = {
    'DPPI': (
        'Strategic plans & sector reviews',
        'Policies, circulars & SOPs',
        'HMIS/DHIS2 reports & standards',
        'Donor coordination & workplans',
        'M&E and survey reports',
        'Official correspondence',
    ),
    'HRH': (
        'Workforce plans & establishment',
        'Recruitment & appointments',
        'Performance & development',
        'Transfers & deployment',
        'Payroll verification records',
        'Grievance & discipline files',
    ),
    'PHARMA': (
        'Procurement & tenders',
        'Stock, LMIS & distribution',
        'Cold chain compliance',
        'QA, recalls & destruction',
        'Supplier contracts',
        'Donations & emergency stock',
    ),
    'DPC': (
        'IDSR & surveillance reports',
        'Outbreak investigation & response',
        'Immunization programme records',
        'NCD & health promotion',
        'Epidemic bulletins',
        'Partner coordination (DPC)',
    ),
    'HLS': (
        'Hospital service agreements',
        'Lab QA & accreditation',
        'Medical equipment maintenance',
        'Referral & ambulance coordination',
        'Facility projects & infrastructure',
    ),
    'PPR': (
        'Research & ethics submissions',
        'Operational research outputs',
        'Policy briefs & analysis',
        'Programme evaluations',
    ),
    'ADMIN_FIN': (
        'Budget & fiscal reports',
        'Payments & imprest',
        'Audit reports & responses',
        'Assets & inventory',
        'Travel & logistics approvals',
    ),
}

# Each entry: (short_code, cabinet_label, full_name)
MOHS_DIRECTORATES = (
    (
        'DPPI',
        'Directorate of Planning, Policy and Information (DPPI)',
        'Directorate of Planning, Policy and Information',
    ),
    (
        'HRH',
        'Directorate of Human Resources for Health (HRH)',
        'Directorate of Human Resources for Health',
    ),
    (
        'PHARMA',
        'Directorate of Pharmaceuticals and Medical Supplies',
        'Directorate of Pharmaceuticals and Medical Supplies',
    ),
    (
        'DPC',
        'Directorate of Disease Prevention and Control',
        'Directorate of Disease Prevention and Control',
    ),
    (
        'HLS',
        'Directorate of Hospital and Laboratory Services',
        'Directorate of Hospital and Laboratory Services',
    ),
    (
        'PPR',
        'Directorate of Policy, Planning and Research',
        'Directorate of Policy, Planning and Research',
    ),
    (
        'ADMIN_FIN',
        'Directorate of Administration and Finance',
        'Directorate of Administration and Finance',
    ),
)
