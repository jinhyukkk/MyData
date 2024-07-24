// 엔터 키를 눌렀을 때 검색 버튼 클릭 이벤트 처리
function handleEnterKeyPress(event) {
    if (event.key === 'Enter') {
        // 검색 버튼을 클릭
        document.getElementById('searchBtn').click();
    }
}


// 검색 조회
function getMyPortfolio() {
    $('#tableBody').empty();
    // 로딩 인디케이터 표시
    loadingIndicator.style.display = 'block';
    $.ajax({
        url: "/api/myPortfolio",
        type: "GET",
        contentType: 'application/json',
        success: function (response) {
            if (response.message === 'Success') {
                console.log(response.result)
                setTableData(response.result);
            } else if ($.isEmptyObject(response.result)) {
                alert('결과가 없습니다.');
            } else {
                alert('조회 실패');
            }

            // 로딩 인디케이터 숨김
            loadingIndicator.style.display = 'none';
        },
        error: function (error) {
            // console.log("Error:", error);
            // 로딩 인디케이터 숨김
            loadingIndicator.style.display = 'none';
        }
    });
}

function setTableData(data) {
    // 테이블에 데이터 추가하기
    var tableBody = document.getElementById('tableBody');
    data.forEach(function (item) {
        const row = tableBody.insertRow();
        const stockNameCell = row.insertCell(0);
        const quantityCell = row.insertCell(1);
        const averagePriceCell = row.insertCell(2);
        const currentPriceCell = row.insertCell(3);
        const purchaseAmountCell = row.insertCell(4);
        const valuationAmountCell = row.insertCell(5);
        const profitAndLossCell = row.insertCell(6);
        const returnRatioCell = row.insertCell(7);
        const evaluationRatioCell = row.insertCell(8);
        const actionsCell = row.insertCell(9);

        stockNameCell.textContent = item.stockName;
        quantityCell.textContent = item.quantity;
        averagePriceCell.textContent = item.averagePrice;
        currentPriceCell.textContent = item.currentPrice;
        purchaseAmountCell.textContent = item.purchaseAmount;
        valuationAmountCell.textContent = item.valuationAmount;
        profitAndLossCell.textContent = item.profitAndLoss;
        returnRatioCell.textContent = item.returnRatio;
        evaluationRatioCell.textContent = item.evaluationRatio;

        // 저장 버튼 추가
        const saveButton = document.createElement('button');
        saveButton.type = 'button';
        saveButton.textContent = '저장';
        saveButton.addEventListener('click', function () {
            // 저장 버튼 클릭 시 실행할 코드
            const row = $(this).closest('tr');

            // 각 셀 (td) 의 내용을 변수에 저장합니다.
            const stockName = row.find('td:eq(0)').text();
            const quantity = row.find('td:eq(1)').text();
            const averagePrice = row.find('td:eq(2)').text();
            const currentPrice = row.find('td:eq(3)').text();
            const purchaseAmount = row.find('td:eq(4)').text();
            const valuationAmount = row.find('td:eq(5)').text();
            const profitAndLoss = row.find('td:eq(6)').text();
            const returnRatio = row.find('td:eq(7)').text();
            const evaluationRatio = row.find('td:eq(8)').text();

            $.ajax({
                url: '/api/myPortfolio',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    stockName: stockName,
                    quantity: quantity,
                    averagePrice: averagePrice,
                    currentPrice: currentPrice,
                    purchaseAmount: purchaseAmount,
                    valuationAmount: valuationAmount,
                    profitAndLoss: profitAndLoss,
                    returnRatio: returnRatio,
                    evaluationRatio: evaluationRatio
                }),
                success: function (response) {
                    showToast(response.message);
                },
                error: function (xhr, status, error) {
                    console.error('Error:', error);
                    alert('저장에 실패했습니다.');
                }
            });
        });

        actionsCell.appendChild(saveButton);
    });
}

function showToast(message) {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerText = message;

    const container = document.getElementById('toast-container');
    container.appendChild(toast);

    requestAnimationFrame(() => {
        toast.classList.add('show');
    });

    setTimeout(() => {
        toast.classList.remove('show');
        toast.classList.add('hide');
        // Remove the element from the DOM after animation ends
        toast.addEventListener('animationend', () => {
            toast.remove();
        });
    }, 3000);
}

// scripts.js
document.addEventListener("DOMContentLoaded", () => {
    const searchBtn = document.getElementById("searchBtn");
    const toggleButton = document.getElementById("toggleButton");
    const inputBox = document.getElementById("inputBox");
    const closeButton = document.getElementById("closeButton");
    const stockForm = document.getElementById("stockForm");

    searchBtn.addEventListener("click", () => {
        getMyPortfolio();
    });

    toggleButton.addEventListener("click", () => {
        if (inputBox.classList.contains("hidden")) {
            inputBox.classList.remove("hidden");
        } else {
            inputBox.classList.add("hidden");
        }
    });

    closeButton.addEventListener("click", () => {
        inputBox.classList.add("hidden");
    });

    stockForm.addEventListener("submit", (e) => {
        e.preventDefault();
        // FormData 객체 생성
        const formData = new FormData(stockForm);
        // FormData를 JSON으로 변환
        const jsonObject = {};
        formData.forEach((value, key) => {
            jsonObject[key] = value;
        });

        $.ajax({
        url: "/api/myPortfolio",
        type: "POST",
        contentType: 'application/json',
                data: JSON.stringify(jsonObject),
        success: function (response) {
            if (response.message === 'Success') {
                console.log(response.result)
                getMyPortfolio();
            } else if ($.isEmptyObject(response.result)) {
                alert('결과가 없습니다.');
            } else {
                alert('조회 실패');
            }

            // 로딩 인디케이터 숨김
            loadingIndicator.style.display = 'none';
        },
        error: function (error) {
            // console.log("Error:", error);
            // 로딩 인디케이터 숨김
            loadingIndicator.style.display = 'none';
        }
    });


        // alert(`Saved: ${userInput}`);
        // 실제로 데이터를 저장하려면 AJAX 요청 등을 추가할 수 있습니다.
        inputBox.classList.add("hidden");
    });
});
