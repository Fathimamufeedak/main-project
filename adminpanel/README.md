# Admin Module — Medicinal Plant Identification (Phase-1)

## Purpose
This admin module provides a secure, role-based dashboard for site administrators to manage Doctors, Users, Plants, Remedies, Consultations, and a Dataset placeholder for Phase‑2 ML work.

## Authentication & Access
- Admin login (email + password) via `/adminpanel/login/`.
- Only users with `is_staff=True` can access the admin panel.
- Session-based authentication (Django auth + `admin_required` decorator used by views).

## Key Features
- Dashboard: overview cards (Total Users, Total Doctors, Pending Approvals, Total Plants, Total Consultations).
- Doctor Approval: view, approve, reject doctor registrations; show status badges (Pending / Approved / Rejected).
- User Management: list, search, view details, deactivate users; view user consultation history.
- Doctor Management: list approved doctors, edit details, remove doctor record, view remedies by doctor.
- Plant Management (CRUD): add, edit, delete, and list plant records.
- Remedy Management (CRUD): add/edit/delete remedies and link them to a Plant and (optionally) a Doctor.
- Consultation Management: read-only listing of consultations with user, doctor, symptoms, image, status, and timestamp.
- Dataset Management: upload plant images to `MEDIA_ROOT/dataset/` (no ML processing in Phase‑1).

## File Locations (important)
- Views: `adminpanel/views.py`
- URLs: `adminpanel/urls.py`
- Templates: `templates/adminpanel/` (dashboard, login, doctors, users, plants, remedies, consultations, dataset)
- Styles: `static/css/style.css`

## Admin Workflow (high level)
1. Admin signs in at `/adminpanel/login/`.
2. Dashboard provides summary stats and quick links.
3. Admin reviews `Approve Doctors` to accept or reject registrations.
4. Admin manages users, edits or deactivates accounts if necessary.
5. Admin manages plant information and remedies (CRUD operations).
6. Admin reviews consultations for monitoring purposes.
7. Admin uploads dataset images via `Dataset Management` (files saved to `MEDIA_ROOT/dataset/`).

## Screens Explanation (for viva)
- Dashboard: Cards showing counts and quick navigation buttons to each management area.
- Approve Doctors: Table with doctor profile info, qualification, experience, current status, and action buttons to approve/reject.
- Manage Users: Searchable user table; buttons to view details and deactivate accounts. User detail view includes consultation history.
- Manage Doctors: Table of doctors with edit/remove actions and a link to view remedies contributed by each doctor.
- Manage Plants: CRUD interface for plant entries using form cards for input; tables show plant summaries.
- Manage Remedies: Add remedial instructions connected to a plant and optionally to a doctor. Table lists remedies with edit/delete.
- Consultations: Read-only chronological list showing who submitted, assigned doctor, symptoms, image link and status.
- Dataset Management: Simple uploader for collecting labeled plant images for Phase‑2. Shows uploaded filenames.

## Notes & Assumptions
- Uses Django's default `User` model; `is_staff` denotes admin privileges to avoid changing existing auth.
- Dataset uploads are stored on the filesystem under `MEDIA_ROOT/dataset/`.
- No ML or model training is implemented in Phase‑1 as required.

## Next steps (optional enhancements)
- Add pagination and filters for large lists.
- Add unit tests for admin views and permissions.
- Add an audit log for admin actions (approvals, deletions).
- Add thumbnails/previews for dataset images in the UI.

---

If you want, I can now:
- Commit these changes and prepare a short demo walkthrough, or
- Add unit tests for critical admin views, or
- Implement pagination and search improvements.
