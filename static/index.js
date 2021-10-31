function handleAlerts(type, msg, num){
    /*
    Parameters:
    type: the type of alert one wants displayed
    msg: the message one wants displayed
    num: string of the number designating what specific alert box we
         want alert sent to

    Returns an alert written in html using boostrap
    */
    const alertBox = document.getElementById('alert-box-' + num);
    console.log(msg);
    alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${msg}
        </div>
    `
}
