// static/js/board.js
function showUploadForm(event) {
    event.stopPropagation();  // 이벤트가 상위 요소로 전달되지 않도록 함
    document.getElementById('upload-form').classList.remove('hidden');
}

function closeForm() {
    document.getElementById('upload-form').classList.add('hidden');
}

document.getElementById('create-comment-btn').addEventListener('click', function() {
    // 버튼에서 data- 속성을 통해 값을 가져옴
    var goal = this.getAttribute('data-goal');
    var duration = this.getAttribute('data-duration');
    var username = this.getAttribute('data-username');
    var uploadImgUrl = this.getAttribute('data-uploadimgurl');

    // 값이 제대로 넘어오는지 콘솔에서 확인
    console.log(goal, duration, username, uploadImgUrl);

    // createComment 함수 호출
    createComment(goal, duration, username, uploadImgUrl);
});

function showStory(element) {
    var popup = document.getElementById('story-popup');
    var popupImg = document.getElementById('popup-img');
    var uploadUrl = document.getElementById('upload-url');

    // Get the uploaded image URL from data attribute
    var uploadImage = element.getAttribute('data-upload-img');
    

    if (uploadImage && uploadImage.trim() !== '' && uploadImage !== 'None') {
        // Set the uploaded image URL in the popup if it exists
        popupImg.src = uploadImage;
        // uploadUrl.innerText = "업로드된 이미지 URL: " + uploadImage;
    } else {
        // 캐릭터 이미지가 있는 경우 이를 표시
        var characterImage = element.querySelector('img');
        if (characterImage) {
            popupImg.src = characterImage.getAttribute('src');
            // uploadUrl.innerText = "캐릭터 이미지 URL: " + characterImage.getAttribute('src');
        } else {
            console.error("캐릭터 이미지를 찾을 수 없습니다.");
        }
    }
    popup.classList.remove('hidden');
}

function closePopUp() {
    document.getElementById('story-popup').classList.add('hidden');
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


function createComment(goal, duration, username, uploadImgUrl) {
    
    console.log("createComment 함수가 호출되었습니다.");
    console.log("Goal:", goal);
    console.log("Duration:", duration);
    console.log("Username:", username);
    console.log("Upload Image URL:", uploadImgUrl);

    const formData = new FormData();
    formData.append('img_src', uploadImgUrl || document.getElementById('popup-img').getAttribute('src'));
    formData.append('goal', goal);
    formData.append('duration', duration);
    formData.append('username', username);

    fetch(storyQueryUrl,{
    // fetch("{% url '/openai/story_query/' %}", {  // AJAX로 POST 요청
        method: "POST",
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken  // CSRF 토큰 포함
        },
    })
    .then(response => {
        // 응답이 JSON 형태로 오지 않으면 에러 처리
        if (!response.ok) {
            // 디버그
            response.text().then(text=>{
                console.log("HTTP 상태 코드:", response.status);
                console.log("응답테스트:", text);
            })
            throw new Error("HTTP error, status = " + response.status);
        }
        return response.json();  // JSON 응답 파싱
    })
    .then(data => {
        // 응답 데이터를 HTML에 표시
        console.log("OpenAI 응답 데이터:", data);
        document.getElementById('openai-comment').textContent = data.response || "결과 없음";
    })
    .catch(error => {
        console.error("OpenAI 요청에서 오류 발생:", error);
        document.getElementById('openai-comment').textContent = "OpenAI 요청 실패: " + error.message;
    });
}

