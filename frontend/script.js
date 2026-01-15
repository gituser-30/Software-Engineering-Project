function sendOTP() {
    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };
    fetch("http://127.0.0.1:8000/register/send-otp", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    }).then(r => r.json()).then(d => {
        alert(d.message);
        document.getElementById("otpSection").style.display="block";
    });
}

function verifyOTP() {
    const email=document.getElementById("email").value;
    const otp=document.getElementById("otp").value;
    fetch(`http://127.0.0.1:8000/register/verify-otp/${email}/${otp}`, {method:"POST"})
    .then(r=>r.json()).then(d=>{
        alert(d.message);
        window.location.href="index.html";
    });
}

function login() {
    const data={
        email:document.getElementById("email").value,
        password:document.getElementById("password").value
    };
    fetch("http://127.0.0.1:8000/login",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify(data)
    }).then(r=>r.json()).then(d=>{
        if(d.user){
            localStorage.setItem("user",JSON.stringify(d.user));
            window.location.href="profile.html";
        } else alert(d.detail);
    });
}
