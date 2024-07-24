// 엔터 키를 눌렀을 때 검색 버튼 클릭 이벤트 처리
function handleEnterKeyPress(event) {
    if (event.key === 'Enter') {
        // 검색 버튼을 클릭
        document.getElementById('searchBtn').click();
    }
}

// 검색 조회
function getPublicStocks() {
    $('#tableBody').empty();
    // 로딩 인디케이터 표시
    loadingIndicator.style.display = 'block';
    $.ajax({
        url: "/api/publicStocks",
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
        const companyNameCell = row.insertCell(0);
        const subDateCell = row.insertCell(1);
        const refundDateCell = row.insertCell(2);
        const openDateCell = row.insertCell(3);
        const publicPriceCell = row.insertCell(4);
        const predictionRateCell = row.insertCell(5);
        const jugansaCell = row.insertCell(6);
        const actionsCell = row.insertCell(7);

        companyNameCell.textContent = item.companyName;
        subDateCell.textContent = item.subDate;
        refundDateCell.textContent = item.refundDate;
        openDateCell.textContent = item.openDate;
        publicPriceCell.textContent = item.publicPrice;
        predictionRateCell.textContent = item.predictionRate;
        jugansaCell.textContent = item.jugansa;

        // 저장 버튼 추가
        const saveButton = document.createElement('button');
        saveButton.type = 'button';
        saveButton.textContent = '저장';
        saveButton.addEventListener('click', function () {
            // 저장 버튼 클릭 시 실행할 코드
            const row = $(this).closest('tr');

            // 각 셀 (td) 의 내용을 변수에 저장합니다.
            const companyName = row.find('td:eq(0)').text();
            const subDate = row.find('td:eq(1)').text();
            const refundDate = row.find('td:eq(2)').text();
            const openDate = row.find('td:eq(3)').text();
            const publicPrice = row.find('td:eq(4)').text();
            const predictionRate = row.find('td:eq(5)').text();
            const jugansa = row.find('td:eq(6)').text();

            $.ajax({
                url: '/api/publicStocks',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    companyName: companyName,
                    subDate: subDate,
                    refundDate: refundDate,
                    openDate: openDate,
                    publicPrice: publicPrice,
                    predictionRate: predictionRate,
                    jugansa: jugansa
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

$(document).ready(function () {
    $("#searchBtn").click(function () {
        getPlaceData();
    });

    $("#getPublicStocks").click(function () {
        getPublicStocks();
    });

    //페이지 이동
    $("#moveSavedPage").click(function () {
        location.href = 'savedList.html'
    });
});