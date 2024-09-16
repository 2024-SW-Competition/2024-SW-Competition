/* 보드게임판 js */
/* story 부분 */
function showStory(element){
    var uploadImage = element.querySelector('img').getAttribute('src');
    var popup = document.getElementById("story-popup");
    var popupImg = document.getElementById("popup-img");

    popupImg.src = uploadedImage;
    popup.style.display = "block";
}
function closePopUp(){
    var popup = document.getElementById("story-popup");
    popup.style.display = "none";
}
function openForm() {
    document.getElementById('upload-form').classList.add('active');
}

function closeForm() {
    document.getElementById('upload-form').classList.remove('active');
}