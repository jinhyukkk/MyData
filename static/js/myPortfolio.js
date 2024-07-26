class PortfolioManager {
    constructor() {
        this.loadingIndicator = document.getElementById('loadingIndicator');
        this.exTbody = document.getElementById('exTbody');
        this.krTableBody = document.getElementById('krTableBody');
        this.usTableBody = document.getElementById('usTableBody');
        this.jpTableBody = document.getElementById('jpTableBody');
        this.searchBtn = document.getElementById('searchBtn');
        this.addItemButton = document.getElementById('addItemButton');
        this.inputBox = document.getElementById('inputBox');
        this.closeButton = document.getElementById('closeButton');
        this.stockForm = document.getElementById('stockForm');
        this.toastContainer = document.getElementById('toast-container');

        this.init();
    }

    init() {
        this.bindEvents();
        this.getMyPortfolio();
        this.getExchangeRates();
    }

    bindEvents() {
        this.searchBtn.addEventListener('click', () => this.getMyPortfolio());
        this.addItemButton.addEventListener('click', () => this.toggleInputBox());
        this.closeButton.addEventListener('click', () => this.toggleInputBox(true));
        this.stockForm.addEventListener('submit', (e) => this.addStock(e));
        document.addEventListener('keydown', (e) => this.handleEnterKeyPress(e));
    }

    handleEnterKeyPress(event) {
        if (event.key === 'Enter') {
            this.searchBtn.click();
        }
    }

    getExchangeRates() {
        $.ajax({
            url: "/api/exchangeRates",
            type: "GET",
            contentType: 'application/json',
            success: (response) => this.handleExchangeRatesResponse(response),
            error: () => this.hideLoadingIndicator()
        });
    }

    handleExchangeRatesResponse(response) {
        if (response.message === 'Success') {
            this.setExTableData(response.result);
        } else if ($.isEmptyObject(response.result)) {
            alert('환율 조회 결과가 없습니다.');
        } else {
            alert('환율 조회 실패');
        }
        this.hideLoadingIndicator();
    }

    setExTableData(data) {
        data.forEach((item) => {
            let row = this.exTbody.insertRow();
            this.createExTableCells(row, item);
        });
    }

    createExTableCells(row, item) {
        const cellValues = [item.targetCurrency, item.exchangeRate];

        cellValues.forEach((value) => {
            const cell = row.insertCell();
            cell.textContent = value;
        });

        this.createExActionButton(row, item);
    }

    createExActionButton(row, item) {
        const actionsCell = row.insertCell();
        const saveButton = document.createElement('button');
        saveButton.type = 'button';
        saveButton.textContent = '삭제';
        saveButton.id = item.idx;
        saveButton.addEventListener('click', () => this.handleExDeleteButtonClick(row));

        actionsCell.appendChild(saveButton);
    }

    // 삭제 API
    handleExDeleteButtonClick(row) {
        if (!confirm("삭제하시겠습니까?")) {
            return false;
        }

        const button = event.target;
        const idx = button.id;

        $.ajax({
            url: '/api/exchangeRates',
            type: 'DELETE',
            contentType: 'application/json',
            data: JSON.stringify({idx: idx}),
            success: (response) => {
                if (response.message === 'Success') {
                    this.getMyPortfolio();
                } else {
                    alert('실패했습니다.');
                }
            },
            error: (xhr, status, error) => {
                console.error('Error:', error);
                alert('실패했습니다.');
            }
        });
    }
    getMyPortfolio() {
        this.getPortfolioByNation('KR');
        this.getPortfolioByNation('US');
        this.getPortfolioByNation('JP');
    }


    getPortfolioByNation(nation = 'KR') {
        this.krTableBody.innerHTML = ''; // Clear existing table data
        this.showLoadingIndicator();
        const queryString = $.param({nation: nation, sort: 'sort'});
        $.ajax({
            url: "/api/myPortfolio",
            type: "GET",
            contentType: 'application/json',
            data: queryString,
            success: (response) => this.handlePortfolioResponse(response),
            error: () => this.hideLoadingIndicator()
        });
    }


    handlePortfolioResponse(response) {
        if (response.message === 'Success') {
            this.setTableData(response.result, response.nation);
        } else if ($.isEmptyObject(response.result)) {
            alert('결과가 없습니다.');
        } else {
            alert('조회 실패');
        }
        this.hideLoadingIndicator();
    }

    setTableData(data, nation) {
        data.forEach((item) => {
            let row = '';
            if (nation === 'KR') {
                row = this.krTableBody.insertRow();
            } else if (nation === 'US') {
                row = this.usTableBody.insertRow();
            } else if (nation === 'JP') {
                row = this.jpTableBody.insertRow();
            }
            this.createTableCells(row, item);
        });
    }

    createTableCells(row, item) {
        const cellValues = [
            item.stockName, item.quantity, item.averagePrice,
            item.currentPrice, item.purchaseAmount, item.valuationAmount,
            item.profitAndLoss, item.returnRatio, item.evaluationRatio
        ];

        cellValues.forEach((value, index) => {
            const cell = row.insertCell();
            cell.textContent = value;
            if (index !== 0) {
                cell.style.textAlign = 'right';
            }
        });

        this.createActionButton(row, item);
    }

    createActionButton(row, item) {
        const actionsCell = row.insertCell();
        const saveButton = document.createElement('button');
        saveButton.type = 'button';
        saveButton.textContent = '삭제';
        saveButton.id = item.idx;
        saveButton.addEventListener('click', () => this.handleDeleteButtonClick(row));

        actionsCell.appendChild(saveButton);
    }

    // 삭제 API
    handleDeleteButtonClick(row) {
        if (!confirm("삭제하시겠습니까?")) {
            return false;
        }

        const button = event.target;
        const idx = button.id;

        $.ajax({
            url: '/api/myPortfolio',
            type: 'DELETE',
            contentType: 'application/json',
            data: JSON.stringify({idx: idx}),
            success: (response) => {
                if (response.message === 'Success') {
                    this.getMyPortfolio();
                } else {
                    alert('실패했습니다.');
                }
            },
            error: (xhr, status, error) => {
                console.error('Error:', error);
                alert('실패했습니다.');
            }
        });
    }

    addStock(event) {
        event.preventDefault();

        const formData = new FormData(this.stockForm);
        const jsonObject = {};
        formData.forEach((value, key) => {
            jsonObject[key] = value;
        });

        $.ajax({
            url: "/api/myPortfolio",
            type: "POST",
            contentType: 'application/json',
            data: JSON.stringify(jsonObject),
            success: (response) => {
                if (response.message === 'Success') {
                    this.getMyPortfolio();
                } else if ($.isEmptyObject(response.result)) {
                    alert('결과가 없습니다.');
                } else {
                    alert('조회 실패');
                }
                this.hideLoadingIndicator();
            },
            error: () => this.hideLoadingIndicator()
        });

        this.toggleInputBox(true);
    }

    toggleInputBox(hide = false) {
        if (hide) {
            this.inputBox.classList.add('hidden');
            this.addItemButton.classList.remove('hidden');
        } else {
            this.inputBox.classList.toggle('hidden');
            this.addItemButton.classList.toggle('hidden');
        }
    }

    showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerText = message;

        this.toastContainer.appendChild(toast);
        requestAnimationFrame(() => toast.classList.add('show'));

        setTimeout(() => {
            toast.classList.remove('show');
            toast.classList.add('hide');
            toast.addEventListener('animationend', () => toast.remove());
        }, 3000);
    }

    showLoadingIndicator() {
        this.loadingIndicator.style.display = 'block';
    }

    hideLoadingIndicator() {
        this.loadingIndicator.style.display = 'none';
    }
}

// Initialize the PortfolioManager when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => new PortfolioManager());
