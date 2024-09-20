/* 보드게임판 js */
/* story 부분 */
function showStory(element){
    var popup = document.getElementById("story-popup");
    var popupImg = document.getElementById("popup-img");

    var uploadImage = "{{ upload_img }}";

    if (uploadImage) {
        popupImg.src = uploadImage;
    }else{
        var characterImage = element.querySelector('img').getAttribute('src');
        popupImg.src = characterImage;  // Display the character image instead
    }
    popup.style.display = "block";  // Open the popup
}
function closePopUp(){
    var popup = document.getElementById("story-popup");
    popup.style.display = "none";
}
function showUploadForm(event){
    event.stopPropagation();
    document.getElementById('upload-form').style.display = 'block';
}
function closeForm() {
    document.getElementById('upload-form').classList.remove('active');
}