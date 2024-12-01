/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project
// 페이지 로드 시 모든 이벤트를 초기화
document.addEventListener('DOMContentLoaded', function () {
    setupLoginForm();
    setupLogoutButton();
    addCart();
    Order();
});

// 로그인 폼 처리
function setupLoginForm() {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            event.preventDefault(); // 기본 폼 제출 방지

            const formData = new FormData(loginForm);
            fetch('/login/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCsrfToken(), // CSRF 토큰 추가
                },
            })
                .then(response => response.json().then(data => ({ status: response.ok, data }))) // 응답 상태와 데이터 처리
                .then(({ status, data }) => {
                    if (status) {
                        alert(data.message); // 성공 메시지
                        window.location.href = '/mainpage_after'; // 성공 시 이동
                    } else {
                        alert(data.message || '로그인에 실패했습니다.'); // 에러 메시지 출력
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('서버와의 통신 오류가 발생했습니다.');
                });
        });
    }
}

// 로그아웃 버튼 처리
function setupLogoutButton() {
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', function () {
            fetch('/logout/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(), // CSRF 토큰 추가
                },
            })
                .then(response => {
                    if (response.ok) {
                        alert('로그아웃 되었습니다!');
                        window.location.href = '/mainpage_before'; // 로그아웃 후 리다이렉트
                    } else {
                        alert('로그아웃에 실패했습니다.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('서버와의 통신 오류가 발생했습니다.');
                });
        });
    }
}

function addCart() {
    const cartButtons = document.querySelectorAll('.cart-button');

    cartButtons.forEach(button => {
        button.addEventListener('click', function () {
            const menuId = button.getAttribute('data-menu-id');
            console.log('Button clicked, menuId:', menuId); // 버튼 클릭 시 메뉴 ID 로그

            fetch('/addcart/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ menu_id: menuId }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert(data.message);
                    } else {
                        alert('카트 추가 실패: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('서버와의 통신 오류가 발생했습니다.');
                });
        });
    });
}

function Order() {
    const orderButton = document.getElementById("order-button");  // 주문하기 버튼

    // 주문하기 버튼 클릭 시 처리
    orderButton.addEventListener('click', function (event) {
        event.preventDefault(); // 기본 폼 제출을 방지

        // CSRF 토큰을 가져오는 함수 호출 (기존에 구현되어 있다고 가정)
        const csrfToken = getCsrfToken();

        // 서버에 POST 요청 보내기
        fetch('/order/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // 주문이 완료되면 사용자에게 메시지 표시
                    alert(data.message);
                    window.location.href = '/mainpage_after';
                } else {
                    alert('주문 실패: ' + data.message);
                }
            })
            .catch(error => {
                console.error('주문 중 오류 발생:', error);
                alert('서버와의 통신 중 오류가 발생했습니다.');
            });
    });
};

// CSRF 토큰 가져오기
function getCsrfToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];

    return cookieValue || '';
}

