async function addSalary() {
  const amount = parseFloat(document.getElementById('salaryAmount').value);
  if (!amount) return alert("Enter valid salary");

  const res = await fetch('http://127.0.0.1:5000/add_income', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ amount })
  });

  const data = await res.json();
  alert("Salary added. Remaining: ₹" + data.remaining_salary);

  // Clear the salary input
  document.getElementById('salaryAmount').value = '';
  loadSummary();
}

async function addExpense() {
  const desc = document.getElementById('expenseDesc').value.trim();
  const amount = parseFloat(document.getElementById('expenseAmount').value);
  if (!desc || !amount) return alert("Enter valid expense description and amount");

  const res = await fetch('http://127.0.0.1:5000/add_expense', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ description: desc, amount })
  });

  const data = await res.json();
  alert(`Expense added under category: ${data.category}. Remaining: ₹${data.remaining_salary}`);

  // Clear the expense input fields
  document.getElementById('expenseDesc').value = '';
  document.getElementById('expenseAmount').value = '';
  loadSummary();
}

async function loadSummary() {
  const res = await fetch('http://127.0.0.1:5000/summary');
  const data = await res.json();

  document.getElementById('income').textContent = data.income;
  document.getElementById('expenses').textContent = data.expenses;
  document.getElementById('remaining').textContent = data.remaining_salary;
  document.getElementById('alert').textContent = data.alert;
}

// Load summary on page load
loadSummary();
