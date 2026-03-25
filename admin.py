{% extends "base.html" %}
{% block title %}Students{% endblock %}
{% block page_title %}Students{% endblock %}

{% block content %}
<div class="page-header">
  <div class="page-title">All Students <span class="text-muted text-sm" style="font-weight:400">({{ rows|length }})</span></div>
  <button class="btn btn-primary" onclick="document.getElementById('addModal').classList.add('open')">
    + Add Student
  </button>
</div>

<!-- Search bar -->
<div style="margin-bottom:16px">
  <input type="text" class="form-control" id="searchInput" placeholder="Search by name or ID…" oninput="filterTable()" style="max-width:340px">
</div>

<div class="card">
  <div class="tbl-wrap">
    <table id="studentTable">
      <thead><tr>
        <th>Student ID</th><th>Name</th><th>Batch</th>
        <th>Attempts</th><th>Avg Error%</th><th>Avg WPM</th>
        <th>Best Error%</th><th>Last Test</th><th></th>
      </tr></thead>
      <tbody>
      {% for r in rows %}
      <tr data-search="{{ r.name|lower }} {{ r.id|lower }}">
        <td class="muted">{{ r.id }}</td>
        <td><strong>{{ r.name }}</strong></td>
        <td class="muted">{{ r.batch or '—' }}</td>
        <td>{{ r.attempts }}</td>
        <td>
          {% if r.avg_error != '-' %}
            {% set e = r.avg_error|float %}
            <span class="badge {% if e <= 5 %}badge-pass{% elif e <= 10 %}badge-mid{% else %}badge-fail{% endif %}">{{ e }}%</span>
          {% else %}<span class="text-muted">—</span>{% endif %}
        </td>
        <td>{{ r.avg_wpm if r.avg_wpm != '-' else '—' }}</td>
        <td class="muted">{{ r.best_error if r.best_error != '-' else '—' }}</td>
        <td class="muted text-sm">{{ r.last_date[:10] if r.last_date != '-' else '—' }}</td>
        <td><a href="{{ url_for('admin.student_profile', student_id=r.id) }}" class="btn btn-outline btn-sm">Profile →</a></td>
      </tr>
      {% else %}
      <tr><td colspan="9" style="text-align:center;padding:24px" class="muted">No students found</td></tr>
      {% endfor %}
      </tbody>
    </table>
  </div>
</div>

<!-- Add Student Modal -->
<div class="modal-overlay" id="addModal">
  <div class="modal">
    <div class="modal-title">Add New Student</div>
    <div class="form-group">
      <label class="form-label">STUDENT ID *</label>
      <input type="text" class="form-control" id="new_sid" placeholder="e.g. STN042">
    </div>
    <div class="form-group">
      <label class="form-label">FULL NAME *</label>
      <input type="text" class="form-control" id="new_name" placeholder="e.g. Ravi Kumar">
    </div>
    <div class="form-group">
      <label class="form-label">BATCH</label>
      <input type="text" class="form-control" id="new_batch" placeholder="e.g. Batch A">
    </div>
    <div class="form-group">
      <label class="form-label">EMAIL</label>
      <input type="email" class="form-control" id="new_email" placeholder="Optional">
    </div>
    <div class="modal-footer">
      <button class="btn btn-outline" onclick="document.getElementById('addModal').classList.remove('open')">Cancel</button>
      <button class="btn btn-primary" onclick="addStudent()">Add Student</button>
    </div>
  </div>
</div>
{% endblock %}

{% block scripts %}
<script>
function filterTable() {
  const q = document.getElementById('searchInput').value.toLowerCase();
  document.querySelectorAll('#studentTable tbody tr[data-search]').forEach(r => {
    r.style.display = r.dataset.search.includes(q) ? '' : 'none';
  });
}

async function addStudent() {
  const sid   = document.getElementById('new_sid').value.trim();
  const name  = document.getElementById('new_name').value.trim();
  const batch = document.getElementById('new_batch').value.trim();
  const email = document.getElementById('new_email').value.trim();
  if (!sid || !name) { showToast('ID and Name are required', 'error'); return; }
  const r = await api("{{ url_for('admin.add_student') }}", {student_id:sid, name, batch, email});
  if (r.status === 'ok') {
    showToast('Student added!');
    setTimeout(() => location.reload(), 1200);
  } else {
    showToast(r.message || 'Error', 'error');
  }
}
</script>
{% endblock %}
