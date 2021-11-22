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
   console.log("here");
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
