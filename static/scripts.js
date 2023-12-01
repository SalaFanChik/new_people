// Подменяем данные пользователя (имя и номер телефона) с сервера
document.querySelector('.username').textContent = 'John Doe';
document.querySelector('.phone-number').textContent = '+1234567890';

// Загружаем данные о кейсах пользователя и отображаем их
const casesData = [
    { name: 'Case 1', case_id: 1 },
    { name: 'Case 2', case_id: 2 },
    // Добавить остальные кейсы
];

const casesSection = document.querySelector('.cases');
casesData.forEach(caseData => {
    const caseElement = document.createElement('div');
    caseElement.classList.add('case');
    caseElement.innerHTML = `<p><strong>Название кейса:</strong> <a href="/case_detail/${caseData.case_id}">${caseData.name}</a></p>`;
    casesSection.appendChild(caseElement);
});
