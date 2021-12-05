function handleAlertsRSVPConflict(num, name, time_start, link){
    /*
    Parameters:
    num: string of the number designating what specific alert box we
         want alert sent to
    name: name of the conflicting workout
    time_start: start time of this workout
    link: link to the workout details page

    Returns an alert written in html using boostrap
    */
    const alertBox = document.getElementById('alert-box-' + num);
    alertBox.innerHTML = `
        <div class="alert alert-danger" role="alert">
            Conflicting workout already RSVP'd for:
            <strong>Name: </strong>${name}
            <strong>Start time: </strong> ${time_start}
            <a href=${link} class="stretched-link"></a>
        </div>
    `
}

function handleRedirectAlerts(msg) {
    /*
     * Parameters:
     * msg: message for redirection
     * 
     * Returns an alert written in html using bootstrap, notifying athlete that they
     * lack permission to view coaches tools
     */
    const permAlertBox = document.getElementById("perm-alert-box");
    permAlertBox.innerHTML = `
        <div class="alert alert-warning d-flex align-items-center" role="alert">
            <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Warning:"><use xlink:href="#exclamation-triangle-fill"/></svg>
            <div>
                ${msg}
            </div>
        </div>
    `
}