const spinner = document.getElementById('loading');
const dBtn = document.querySelector("downloadBtn")
const convert_show = document.getElementById('convert-show');
const convert_button = document.getElementById('button1');

function loadingSpin(time){
    //로딩 표시
    showLoading();
    //로딩 숨기기
    setTimeout("hideLoading()", time);
}
function showLoading(){
    document.getElementById('loading').style.display = 'flex';
}
function hideLoading(){
    document.getElementById('loading').style.display = 'none';
}

function addDownloadBtn(){
    let link = document.createElement("a");
    link.setAttribute('href',"./static/img/after.png");
    link.setAttribute('download', "download");

    let downloadBtn = document.createElement("button");
    downloadBtn.setAttribute("class","convert__button");
    downloadBtn.textContent = '다운로드';
    link.appendChild(downloadBtn);

    convert_show.removeChild(convert_button);
    convert_show.appendChild(link);
}

function borderStress(time){
    console.log('borderStress start');
    const image_border = document.getElementById('image-show');
    image_border.style.border = "10px solid var(--first-color)";
    let checkbox = document.createElement('i');
    checkbox.setAttribute('class', "bx bxs-check-square");
    checkbox.style.display = "flex";
    checkbox.style.color = "var(--first-color)";
    checkbox.style.position = "absolute";
    checkbox.style.width = "100%";
    checkbox.style.height = "100%";
    checkbox.style.justifyContent="center";
    checkbox.style.alignItems="center";
    checkbox.style.textAlign = "center";
    checkbox.style.fontSize = "7rem";
    checkbox.style.transition = ".5s";
    image_border.appendChild(checkbox);
    setTimeout(()=>{
        image_border.style.border = "3px solid var(--text-color-light)";
        image_border.removeChild(checkbox);
    }, time);
}

/*=============== SUBMIT BUTTON ==========================*/
function loadFile(input) {
    let file = input.files[0];	//선택된 파일 가져오기
    //미리 만들어 놓은 div에 text(파일 이름) 추가
    let name = document.getElementById('fileName');
    name.textContent = file.name;

    let container = document.getElementById('image-show');
    console.log(container.hasChildNodes());
    if(container.childElementCount > 1) {
        location.reload();
    } else {
        //새로운 이미지 div 추가
        let newImage = document.createElement("img");
        newImage.setAttribute("class", 'img');

        //이미지 source 가져오기
        newImage.src = URL.createObjectURL(file);
        newImage.style.width = "100%";
        newImage.style.height = "100%";
        newImage.style.visibility = "hidden";   //버튼을 누르기 전까지는 이미지를 숨긴다
        newImage.style.objectFit = "contain";

        //이미지를 image-show div에 추가
        container.style.backgroundColor = "var(--body-color)";
        container.style.border = "3px solid var(--text-color-light)";
        container.style.display = "flex";
        container.style.marginBottom = "0.5rem";
        container.style.padding = "0.35rem 0.35rem 0.35rem 0.35rem";
        container.style.alignItems = "center";
        container.style.justifyContent = "center";
        container.style.borderRadius = "0.75rem";
        container.hasChildNodes()
        container.appendChild(newImage);
        console.log(container.hasChildNodes());
    }
    image_show = document.getElementById('image-show').lastElementChild;
    image_show.style.visibility ="visible";
    const cvbtn = document.getElementById('convert-show');
    cvbtn.style.visibility="visible";
}

function convertShow(){

}

/*=============== CHANGE BACKGROUND HEADER ===============*/
function scrollHeader() {
  const header = document.getElementById("header");
  if (this.scrollY >= 50) header.classList.add("scroll-header");
  else header.classList.remove("scroll-header");
}
window.addEventListener("scroll", scrollHeader);

/*=============== SWIPER POPULAR ===============*/
let swiperPopular = new Swiper(".popular__container", {
  spaceBetween: 32,
  grabCursor: true,
  centeredSlides: false,
  slidesPerView: "auto",
  loop: false,
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
});

/*=============== VALUE ACCORDION ===============*/
const accordionItems = document.querySelectorAll(".value__accordion-item");

accordionItems.forEach((item) => {
  const accordionHeader = item.querySelector(".value__accordion-header");
  accordionHeader.addEventListener("click", () => {
    const openItem = document.querySelector(".accordion-open");

    toggleItem(item);

    if (openItem && openItem !== item) {
      toggleItem(openItem);
    }
  });
});
const toggleItem = (item) => {
  const accordionContent = item.querySelector(".value__accordion-content");

  if (item.classList.contains("accordion-open")) {
    accordionContent.removeAttribute("style");
    item.classList.remove("accordion-open");
  } else {
    accordionContent.style.height = accordionContent.scrollHeight + "px";
    item.classList.add("accordion-open");
  }
};

/*=============== SCROLL SECTIONS ACTIVE LINK ===============*/
const sections = document.querySelectorAll("section[id]");

function scrollActive() {
  const scrollY = window.pageYOffset;
  sections.forEach((current) => {
    const sectionHeight = current.offsetHeight,
      sectionTop = current.offsetTop - 58,
      sectionId = current.getAttribute("id");

    if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
      document
        .querySelector(".nav__menu a[href*=" + sectionId + "]")
        .classList.add("active-link");
    } else {
      document
        .querySelector(".nav__menu a[href*=" + sectionId + "]")
        .classList.remove("active-link");
    }
  });
}
window.addEventListener("scroll", scrollActive);

/*=============== SHOW SCROLL UP ===============*/
function scrollUp() {
  const scrollUp = document.getElementById("scroll-up");
  if (this.scrollY >= 350) {
    scrollUp.classList.add("show-scroll");
  } else scrollUp.classList.remove("show-scroll");
}
window.addEventListener("scroll", scrollUp);

/*=============== DARK LIGHT THEME ===============*/
const themeButton = document.getElementById("theme-button");
const darkTheme = "dark-theme";
const iconTheme = "bx-sun";

const selectedTheme = localStorage.getItem("selected-theme");
const selectedIcon = localStorage.getItem("selected-icon");

const getCurrentTheme = () =>
  document.body.classList.contains(darkTheme) ? "dark" : "light";
const getCurrentIcon = () =>
  themeButton.classList.contains(iconTheme) ? "bx bx-moon" : "bx bx-sun";

if (selectedTheme) {
  document.body.classList[selectedTheme === "dark" ? "add" : "remove"](
    darkTheme
  );
  themeButton.classList[selectedIcon === "bx bx-moon" ? "add" : "remove"](
    iconTheme
  );
}

themeButton.addEventListener("click", () => {
  document.body.classList.toggle(darkTheme);
  themeButton.classList.toggle(iconTheme);
  localStorage.setItem("selected-theme", getCurrentTheme());
  localStorage.setItem("selected-icon", getCurrentIcon);
});

/*=============== SCROLL REVEAL ANIMATION ===============*/
const sr = ScrollReveal({
  origin: "top",
  distance: "60px",
  duration: 2000,
  delay: 350,
  // reset: true
});

sr.reveal(
  `.home__title, .popular__container, .subscribe__container, .footer__container`
);
sr.reveal(`.home__description, .footer__info`, { delay: 500 });
sr.reveal(`.home__search`, { delay: 600 });
sr.reveal(`.home__value`, { delay: 700 });
sr.reveal(`.home__images`, { delay: 800, origin: "bottom" });
sr.reveal(`.logos__img`, { interval: 100 });
sr.reveal(`.value__images, .contact__content`, { origin: "left" });
sr.reveal(`.value__content, .contact__images`, { origin: "right" });

/*===================== NUMBER COUNT ANIMATION =======================*/

/* ==========================IMAGE UPLOAD=============================*/


// let file = document.getElementById('chooseFile');
// file.onchange = function(e) {
//     const currentBtn = document.getElementById("upload__button");
//     const submitBtn = document.getElementById("submit__button");
//     let files = e.target.files;
//     if (files !== null) {
//         console.log(submitBtn);
//         if(currentBtn.style.display !== 'none'){
//             currentBtn.style.display = 'none';
//             submitBtn.style.display = 'flex';
//         } else {
//             currentBtn.style.display = 'flex';
//             submitBtn.style.display = 'none';
//         }
//     }
// }

function page_update() {
    location.reload(true);
  }


/* LOADING SPINNER */
function showSpinner() {
    document.getElementsByClassName('loading')[0].style.display='block';
}
function hideSpinner() {
    document.getElementsByClassName('loading')[0].style.display='none';
}