Doctor Module - Phase 1

Overview

This document describes the Ayurvedic Doctor Module implemented for Phase-1. It focuses on backend, frontend, and UI polish. Machine Learning is not part of this phase.

Workflow

1. Doctor Registration
   - Doctor registers with username, email and password and provides qualification and experience.
   - An account is created and `is_verified` is set to False.
   - Admin must review and set `is_verified=True` from the admin panel before doctor gains access to the dashboard and features.

2. Doctor Login
   - Doctor logs in using the doctor-specific login page.
   - After successful login, if `is_verified=False`, the doctor sees a "pending verification" page and cannot access the dashboard or consultation features.

3. Dashboard and Consultations
  - Once verified, the doctor can view the dashboard showing total, pending and completed consultations.
  - The doctor can open assigned consultations, view user symptoms and uploaded image, submit a textual response, update consultation status and add/update an Ayurvedic remedy linked to the reported symptom.

4. Remedy Management (Updated - Symptom-based)
  - Remedies are now stored in `plants.Remedy` as symptom-based remedies contributed by verified doctors.
  - Each remedy contains: doctor (FK), symptom (text), remedy_description, usage instructions, optional `plant` link, and `created_at` timestamp.
  - Doctors may add a remedy directly from a consultation (the consultation's symptom is pre-filled) or add a general remedy via the "Add Remedies" page.
  - Remedies added by doctors become searchable by users via symptom keywords.

Admin approval explanation

- The admin reviews doctor accounts via the Django admin interface.
- The `Doctor` model includes a boolean `is_verified` field.
- Until `is_verified` is set True by the admin, the doctor will only see the pending page after login and will not be able to access dashboard, consultations, or remedy management.

Page-wise UI explanation (for viva)

- Doctor Register (`templates/doctors/register.html`)
  - Simple registration form capturing username, email, password, qualification and experience.
  - After registration the doctor sees a success message and is instructed to wait for admin approval.

- Doctor Login (`templates/doctors/login.html`)
  - Clean card layout using Bootstrap.
  - On successful login, if account is unverified, a pending message is shown.

- Pending Verification (`templates/doctors/pending.html`)
  - Informational alert telling the doctor that their account is pending admin approval.
  - Provides logout button.

- Dashboard (`templates/doctors/dashboard.html`)
  - Professional, clean layout using green primary color (medical/herbal feel).
  - Cards show total assigned consultations, pending and completed counts.
  - Quick action buttons: My Consultations, Profile.

- Consultations List (`templates/doctors/consultations.html`)
  - Responsive table with hover effect.
  - Status shown with colored badges (warning / primary / success).
  - Thumbnail for uploaded images.

- Consultation Detail (`templates/doctors/consultation_detail.html`)
  - Displays user info, symptoms and image.
  - Response form to send guidance to user.
  - Status form to update (Pending / In Progress / Completed).
  - Remedy section shows existing remedy or link to add one.

-- Remedy Form (`templates/doctors/remedy_form.html`)
  - Form to add or edit a symptom-based remedy. When opened from a consultation the `symptom` field is pre-filled with the user's reported symptoms.
  - Fields: `symptom` (text), `remedy_description` (textarea), `usage` (textarea), optional `plant` (select).

- Profile (`templates/doctors/profile.html`)
  - Edit doctor fields (qualification, experience) and basic user fields (first name, last name, email).
  - Shows verification status (Pending / Approved).

Notes for evaluators

- The module uses session-based authentication via Django's auth system.
- All doctor-only pages check both authentication and `Doctor.is_verified` before granting access.
- Remedies are stored in `doctors.Remedy` (one-to-one with `consultations.Consultation`) to allow future extension for ML-based plant suggestions in Phase-2.

Development notes

- Models: `doctors.models.Doctor`, `doctors.models.Remedy`
- Views: `doctors.views` contains login, logout, register, dashboard, consultation views, remedy form and profile view.
- Forms: `doctors.forms` contains registration, login, profile, remedy, response and status forms.
- Templates: `templates/doctors/` contains the doctor-facing UI files.

Next steps (Phase-2 readiness)

- Add API endpoints for ML integration (plant suggestion service).
- Add richer logging and audit for doctor responses.
- Consider notification system for users on responses and status changes.

