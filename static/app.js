const messages = [
    "Initializing AI...",
    "Starting camera...",
    "Loading profile data...",
    "Preparing dashboard..."
];

let messageIndex = 0;
const loadingText = document.getElementById("loadingText");

setInterval(() => {
    if (!loadingText) return;
    loadingText.innerText = messages[messageIndex];
    messageIndex = (messageIndex + 1) % messages.length;
}, 800);

// Progress loader
let progress = 0;
const progressEl = document.getElementById("progress");
const progressInterval = setInterval(() => {
    progress += 2;
    if (progressEl) progressEl.innerText = progress + '%';
    if (progress >= 100) clearInterval(progressInterval);
}, 20);

const video = document.getElementById("video");
const overlayCanvas = document.getElementById("canvas");
const captureCanvas = document.createElement("canvas");
const loader = document.getElementById("loader");
let recognitionBusy = false;
let welcomeTimer = null;

function setText(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.innerText = value;
    }
}

function hideLoader() {
    if (loader) {
        loader.classList.add("hide-loader");
    }
    clearInterval(progressInterval);
}

navigator.mediaDevices.getUserMedia({
    video: {
        width: { ideal: 960 },
        height: { ideal: 540 },
        frameRate: { ideal: 30, max: 30 }
    }
})
    .then(stream => {
        video.srcObject = stream;

        video.addEventListener("loadedmetadata", () => {
            console.log("Camera started");
            setInterval(captureFrame, 5000);
            setTimeout(hideLoader, 1000);
        });
    })
    .catch(err => {
        console.error("Camera error", err);
        setText("loadingText", "Camera access denied");
    });

function captureFrame() {
    if (recognitionBusy || video.readyState < 2 || video.videoWidth === 0) {
        return;
    }

    recognitionBusy = true;

    const captureWidth = 480;
    const scale = captureWidth / video.videoWidth;
    captureCanvas.width = captureWidth;
    captureCanvas.height = Math.round(video.videoHeight * scale);

    const ctx = captureCanvas.getContext("2d", { willReadFrequently: true });
    ctx.drawImage(video, 0, 0, captureCanvas.width, captureCanvas.height);
    captureCanvas.toBlob(sendFrame, "image/jpeg", 0.72);
}

function sendFrame(blob) {
    if (!blob) {
        recognitionBusy = false;
        return;
    }

    const formData = new FormData();
    formData.append("image", blob);

    fetch("/recognize", {
        method: "POST",
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            renderRecognitionData(data);
        })
        .catch(err => {
            console.error("Fetch error", err);
        })
        .finally(() => {
            recognitionBusy = false;
        });
}

function renderRecognitionData(data) {
    const studentCard = document.getElementById("studentCard");
    const lecturerCard = document.getElementById("lecturerCard");

    if (data.role === "student") {
        studentCard.classList.remove("hidden");
        lecturerCard.classList.add("hidden");

        setText("id", "ID: " + (data.id || "--"));
        setText("name", "Name: " + (data.name || "--"));
        setText("year", "Year: " + (data.year || "--"));
        setText("branch", "Branch: " + (data.branch || "--"));
        setText("section", "Section: " + (data.section || "--"));
        setText("attendance", "Attendance: " + (data.attendance || "--") + "%");
    } else if (data.role === "lecturer") {
        studentCard.classList.add("hidden");
        lecturerCard.classList.remove("hidden");

        setText("lec_id", "ID: " + (data.id || "--"));
        setText("lec_name", "Name: " + (data.name || "--"));
        setText("department", "Department: " + (data.department || "--"));
        setText("subject", "Subject: " + (data.subject || "--"));
        setText("experience", "Experience: " + (data.experience || "--"));
    } else {
        lecturerCard.classList.add("hidden");
        studentCard.classList.remove("hidden");

        setText("id", "ID: --");
        setText("name", "Name: Unknown");
        setText("year", "Role: Unknown");
        setText("branch", "Status: Unrecognized face");
        setText("section", "");
        setText("attendance", "");
    }

    setText("weather", data.weather || "Waiting for weather data");
    setText("temp", data.temp ? data.temp + " C" : "--");
    setText("time", data.time || "");
    setText("date", data.date || "");
    setText("quote", data.quote || "Recognition insights will appear here.");

// Theme toggle
const themeToggle = document.querySelector('.header-theme-toggle');
if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-theme');
        const isDark = document.body.classList.contains('dark-theme');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });
}

    const welcome = document.getElementById("welcome");
    if (data.name && data.name !== "Unknown") {
        welcome.innerText = "Welcome, " + data.name;
        welcome.classList.add("show-welcome");
        clearTimeout(welcomeTimer);
        welcomeTimer = setTimeout(() => {
            welcome.classList.remove("show-welcome");
        }, 2000);
    } else {
        clearTimeout(welcomeTimer);
        welcome.classList.remove("show-welcome");
    }
}

setTimeout(hideLoader, 5000);

const toggleBtn = document.getElementById("themeToggle");
const body = document.getElementById("body");
let darkMode = true;

toggleBtn.addEventListener("click", () => {
    darkMode = !darkMode;
    body.classList.toggle("dark-theme", darkMode);
});

if (overlayCanvas) {
    const ctx = overlayCanvas.getContext("2d");
    ctx.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);
}

if (window.AOS) {
    AOS.init({
        duration: 700,
        once: true
    });
}

const comingCards = document.querySelectorAll(".coming-card");

if (comingCards.length) {
    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("is-visible");
                cardObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.18,
        rootMargin: "0px 0px -80px 0px"
    });

    comingCards.forEach(card => cardObserver.observe(card));
}
