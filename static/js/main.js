// SupportDesk - Main JS

document.addEventListener('DOMContentLoaded', function () {
  // Auto-dismiss alerts after 5s
  document.querySelectorAll('.alert').forEach(function (alert) {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    }, 5000);
  });

  // Confirm before delete
  document.querySelectorAll('[data-confirm]').forEach(btn => {
    btn.addEventListener('click', e => {
      if (!confirm(btn.dataset.confirm)) e.preventDefault();
    });
  });

  // Character counter for description
  const descField = document.querySelector('textarea[name="description"]');
  if (descField) {
    const counter = document.createElement('small');
    counter.className = 'text-muted';
    descField.parentNode.appendChild(counter);
    descField.addEventListener('input', () => {
      counter.textContent = `${descField.value.length} characters`;
    });
  }
});
