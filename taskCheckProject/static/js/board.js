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