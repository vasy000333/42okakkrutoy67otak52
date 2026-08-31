const bukvjru = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789";
const bukvjen = "abcdefghijklmnopqrstuvwxyz0123456789";

let tld = "";

if (Math.random() < 0.47) {
    tld = ".com";
}
if (Math.random() < 0.06) {
    tld = ".ru";
}
if (Math.random() < 0.04) {
    tld = ".org";
}
if (Math.random() < 0.03) {
    tld = ".net";
}
if (Math.random() < 0.02) {
    tld = ".io";
}
if (Math.random() < 0.04) {
    tld = ".xyz";
}
if (Math.random() < 0.05) {
    tld = ".ai";
}

if (tld === "") {
    tld = ".com";
}

const dominnum = Math.floor(Math.random() * 20) + 1;

const protokol1 = [
    "https://",
    "http://",
    "ftp://",
    "",
    "sftp://"
];

let protokol = protokol1[Math.floor(Math.random() * protokol1.length)];

if (Math.random() < 0.95) {
    protokol = "https://";
}
if (Math.random() < 0.04) {
    protokol = "http://";
}

let domin = "";

for (let i = 0; i < dominnum; i++) {
    let dominbuk;

    if (Math.random() < 0.95) {
        dominbuk = bukvjen[Math.floor(Math.random() * bukvjen.length)];
    }

    if (Math.random() < 0.05) {
        dominbuk = bukvjru[Math.floor(Math.random() * bukvjru.length)];
    }

    domin += dominbuk;
}

domin += tld;
domin = protokol + domin;


console.log(domin);

const link = document.getElementById("domainLink");

link.href = domin;
link.textContent = domin;
link.style.color = "green";
