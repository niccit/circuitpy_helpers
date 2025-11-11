# SPDX-License-Identifier: MIT

from datetime import datetime

# Return the current date (DOW) and a formatted full date (DOW, DATE, MONTH, YEAR)
# Get date from system clock
# Store the date (1-31) and if the new query is different update the date to MQTT
# This is for a board that has a system clock, i.e., Raspberrypi
def get_date_from_system():
    now = datetime.now()
    current_date = now.strftime("%d")
    publish_date = now.strftime("%A %d %b %Y")
    return current_date, publish_date

# Convert provided month in numerals to the fully qualified month name
def get_month_name(month):
    pub_month = None
    if month == "12":
        pub_month = "Dec"
    if month == "11":
        pub_month = "Nov"
    if month == "10":
        pub_month = "Oct"
    if month == "09":
        pub_month = "Sept"
    if month == "08":
        pub_month = "Aug"
    if month == "07":
        pub_month = "Jul"
    if month == "06":
        pub_month = "Jun"
    if month == "05":
        pub_month = "May"
    if month == "04":
        pub_month = "Apr"
    if month == "03":
        pub_month = "Mar"
    if month == "02":
        pub_month = "Feb"
    if month == "01":
        pub_month = "Jan"

    return pub_month
