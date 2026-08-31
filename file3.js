{

    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";
    
    let id = "";
    
    for (let i = 0; i < 11; i++) {
        id += chars[Math.floor(Math.random() * chars.length)];
    }
    
    const url = "https://www.youtube.com/watch?v=" + id;
    
    const link = document.getElementById("youtubeLink");
    
    link.href = url;
    link.textContent = url;
    link.style.color = "green";
}
