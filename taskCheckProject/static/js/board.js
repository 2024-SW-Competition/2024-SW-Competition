// static/js/board.js
function showUploadForm(event) {
    event.stopPropagation();  // 이벤트가 상위 요소로 전달되지 않도록 함
    document.getElementById('upload-form').classList.remove('hidden');
}

function closeForm() {
    document.getElementById('upload-form').classList.add('hidden');
}

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

function createComment(goal, duration, username, uploadImgUrl) {
    console.log("createComment 함수가 호출되었습니다.");  // 함수 호출 확인
    console.log("goal:", goal, "duration:", duration, "username:", username, "uploadImgUrl:", uploadImgUrl);  // 전달된 인자 확인
    
    const imgsrc = uploadImgUrl || document.getElementById('popup-img').getAttribute('src');  // 이미지 경로
    console.log("이미지 경로: " + imgsrc);  // 디버깅용


    // OpenAI 요청 보내기
    fetch("{% url 'story_query_view' %}", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({
            'img_src': imgsrc,
            'goal': goal,
            'duration': duration,
            'username': username
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('openai-comment').textContent = data.response;
    })
    .catch(error => {
        console.error("OpenAI 요청에서 오류 발생:", error);
    });
}

