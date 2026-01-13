User Module - Phase 1

Overview

This document describes the User Module updates for Phase-1 focusing on symptom-based remedy search and clean UI.

Workflow

1. Search Remedies
   - Users can enter a symptom keyword (e.g. "cough", "fever") on the "Search Remedies" page.
   - The system searches `plants.Remedy` for matching `symptom` values (case-insensitive substring match) and displays results as cards.
   - Each card shows: Symptom, Remedy description, Usage instructions, optional Plant, and the Doctor who added the remedy.

2. Typical User Flow
   - User logs in -> navigates to "Search Remedies" -> enters symptom -> sees results -> follows remedy guidance.

UI Notes

- Search box is presented as a single-line input plus a green "Search Remedies" button.
- Results are shown as Bootstrap cards (green accents, white background) with doctor attribution and added date.
- User sidebar includes: Dashboard, Search Remedies, My Queries, Profile, Logout.

Role-based access

- The Search Remedies page is available to authenticated users.
- Doctors see a different sidebar (no Upload Plant Image / View Plants links) to prevent mixing of features.

Viva explanation (short)

- Symptom-based remedies: doctors enter remedies tied to symptom descriptions; users search symptoms which returns doctor-contributed remedies. This avoids ML in Phase-1 and keeps the workflow auditable and explainable.

Implementation notes

- Backend: `users.views.search_remedies` queries `plants.Remedy` by `symptom__icontains` and renders `templates/users/search_remedies.html`.
- Models: `plants.Remedy` contains `symptom`, `remedy_description`, `usage`, `doctor` and `created_at` for traceability.

