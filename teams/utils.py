
def is_availible(form_time_start, form_time_end, form_day, item_time_start, item_time_end, item_day):
    '''
    Tells you if schedule conflicts or not with this time
    '''

    # ScheduleItem conflicts with suggested time
    if (form_day == item_day and 
        ((form_time_start <= item_time_start <= form_time_end) or
        (form_time_start <= item_time_end <= form_time_end) or 
        (item_time_start < form_time_start and form_time_end < item_time_end))
    ):
        return True
    else:
         return False