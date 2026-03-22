import flet as ft
from datetime import time, datetime, timedelta

from flet_android_notifications import FletAndroidNotifications
import asyncio
import os



class ClassAlert:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.scroll = ft.ScrollMode.HIDDEN
        self.page.appbar = ft.AppBar(
            title=ft.Text("Class Alert", size=30, weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor=ft.Colors.BLUE_500,
            actions=[
                ft.IconButton(
                     icon=ft.Icons.ALARM_ON,
                     tooltip="test",
                     icon_color=ft.Colors.GREEN,
                     on_click=lambda _: asyncio.create_task(self.test_notification())

                )
            ]
        )

        self.notifications = FletAndroidNotifications()
        self.id_counter = 0

        def next_weekday(day_name, t):
            days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
            today = datetime.now()
            day_num = days.index(day_name)
            days_ahead = day_num - today.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return datetime.combine(today + timedelta(days=days_ahead), t)

        async def add_func(e):
                if  self.date.value == 'None':
                     date_str = "Monday"
                else:
                     date_str = self.date.value     
                
                self.id_counter += 1
                nt_id = self.id_counter
                subject = self.subject_name.value
                grade = self.class_name.value
                date_str = self.date.value
                time_str = self.time_pick.value.strftime("%H:%M")
                dt_str = f"{date_str} {time_str}"
                schld_time = next_weekday(date_str, self.time_pick.value)
                container = ft.Container(
                        padding=ft.Padding.all(10),
                        margin=ft.Margin.all(5),
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment.TOP_LEFT,
                            end=ft.Alignment.BOTTOM_RIGHT,
                            colors=[ft.Colors.BLUE_900, ft.Colors.BLUE_300]
                        ),
                        border_radius=ft.BorderRadius.all(30),
                        content=ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text(f"Class: {self.class_name.value}", size=15, weight=ft.FontWeight.BOLD),
                                        ft.Text(f"Subject: {self.subject_name.value}", size=15, weight=ft.FontWeight.NORMAL),
                                        ft.Text(f"Date: {self.date.value}", size=15, weight=ft.FontWeight.NORMAL),
                                        ft.Text(f"Time: {self.time_pick.value}", size=15, weight=ft.FontWeight.NORMAL),
                                    ],
                                    expand=True,
                                ),
                                ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        tooltip="Delete Entry",
                                        icon_color=ft.Colors.RED_400,
                                        on_click=lambda _: asyncio.create_task(self.cancel_notification(nt_id, cont=container))
                                        )
                                    
                            ]
                        )
                    )

                self.list_timetable.controls.append(
                    container
                )
                self.page.pop_dialog()
                self.page.update()
                await self.save_and_notify_full(nt_id, schld_time, subject, grade)    
                
        
        

        self.subject_name = ft.TextField(label="Subject Name", width=200, hint_text="e.g., Mathematics")
        self.date = ft.Dropdown(
            label="Day",
            options=[
                ft.dropdown.Option("Monday"),
                ft.dropdown.Option("Tuesday"),
                ft.dropdown.Option("Wednesday"),
                ft.dropdown.Option("Thursday"),
                ft.dropdown.Option("Friday"),
                ft.dropdown.Option("Saturday"),
                ft.dropdown.Option("Sunday"),
            ]
         )
        
        self.time_pick = ft.TimePicker(
            confirm_text="Confirm",
            value=time(1, 2),
            entry_mode=ft.TimePickerEntryMode.DIAL,
            help_text="Select the time for the class."
            )
        self.class_name = ft.TextField(label="Class Name", width=200, hint_text="e.g., Grade 10A")

        self.btntime = ft.Button(
            content=ft.Text("Pick Time"),
            on_click=lambda _: self.page.show_dialog(self.time_pick),
        )
                    

        self.addcontrols = ft.ListView(
            controls=[
                self.class_name,
                self.subject_name,
                self.date,
                ft.Text(f"Select Time: {self.time_pick.value}"),
                self.btntime
            ],
            spacing=20,
            scroll=ft.ScrollMode.HIDDEN,
            
        )


        self.add_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add Lessons", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            content=ft.Container(
                content=self.addcontrols,
              ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: self.page.pop_dialog()),
                ft.TextButton("Add", on_click=add_func),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
           
        
            

        self.container = ft.Container(
            padding=ft.Padding.only(left=20, top=25, right=20, bottom=20),
            margin=ft.Margin.all(5),
            expand=True,
            #alignment=ft.Alignment.CENTER,
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=[ft.Colors.BLUE_900, ft.Colors.BLUE_500]
            ),
            border_radius=ft.BorderRadius.all(30),
            
            content=ft.Column(
                controls=[
                    ft.Container(
                        #margin=ft.Margin.only(left=25, top=25),
                        alignment=ft.Alignment.CENTER,
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment.TOP_CENTER,
                            end=ft.Alignment.BOTTOM_CENTER,
                            colors=[ft.Colors.BLUE_700, ft.Colors.BLUE_400]
                        ),
                        border_radius=ft.BorderRadius.all(30),
                        expand=False,
                        width=250,
                        height=30,
                        content=ft.Text(
                            "Smart timetable reminder for teachers",
                            size=13,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.WHITE,
                            expand=True,
                        )
                    ),
                    ft.Text(
                        value="Stay ahead of every class.",
                        size=40,
                        weight=ft.FontWeight.BOLD,
                        #margin=ft.Margin.only(top=5, left=25),
                        color=ft.Colors.WHITE,
                    ),
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        value="Add lessons manually and get reminders before each class starts.",
                                        size=15,
                                        weight=ft.FontWeight.NORMAL,
                                        #margin=ft.Margin.only(top=5, left=25),
                                        color=ft.Colors.WHITE,
                                        expand=True,
                                    )
                                ],
                                expand=True,
                            )
                        ]
                        ),

                    ft.Row(
                        controls=[
                            ft.Button(
                                icon=ft.Icons.CALENDAR_MONTH,
                                content=ft.Text("Add Lessons"),
                                
                                on_click=lambda _: self.page.show_dialog(self.add_dialog),
                                expand=True,
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ]
            )
        )

        self.list_timetable = ft.ListView(
            controls=[
                ft.Text(
                    value="Your Timetable",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_900,
                    text_align=ft.TextAlign.CENTER,
                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM
                )
            ],
            expand=True,
            scroll=ft.ScrollMode.HIDDEN
            
        )

        asyncio.create_task(self.readtimetable())



        self.page.add(
            ft.Row(
                controls=[self.container,],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[self.list_timetable,],
                alignment=ft.MainAxisAlignment.CENTER,
            )

        )
    
    async def save_and_notify_full(self, nt_id: int, schld_time: datetime, subject: str, grade: str):
         try:
              with open("alerts.txt", "a") as f:
                  f.write(f"{nt_id}|{schld_time.isoformat()}|{subject}|{grade}\n")

              await self.notifications.request_permissions()
              await self.notifications.request_exact_alarm_permission()
              await self.notifications.schedule_notification(
                  id=nt_id,
                  title="Class Alert",
                  body=f"Is time for {subject} in {grade} ",
                  scheduled_time=schld_time,
                  play_sound=True,
                  enable_vibration=True,
                  schedule_mode="alarm_clock",
                  
                  
              )

              
         except Exception as e:
              print(f"Error requesting permissions: {e}")
              return
    
    async def test_notification(self):
        try:
            await self.notifications.request_permissions()
            await self.notifications.request_exact_alarm_permission()
            await self.notifications.schedule_notification(
                id=999,
                title="Test Notification",
                body="This is a test notification.",
                scheduled_time=datetime.now() + timedelta(seconds=10),
                play_sound=True,
                enable_vibration=True,
                schedule_mode="alarm_clock",
            )
            await self.notifications.show_notification(
                id=999,
                title="Test Notification",
                body="This is a test notification.",
                play_sound=True,
                enable_vibration=True,
            )
            self.page.show_dialog(ft.SnackBar(
                content=ft.Text("Test notification scheduled! It will appear in 10 seconds."),
                bgcolor=ft.Colors.GREEN_400,
            ))
            print("Test notification scheduled.")
        except Exception as e:
            self.page.show_dialog(ft.SnackBar(
                content=ft.Text("Error scheduling test notification: {e}"),
                bgcolor=ft.Colors.RED_400,
            ))
            print(f"Error scheduling test notification: {e}")


    async def cancel_notification(self, nt_id: int, cont: ft.Container):
        try:
            if os.path.exists("alerts.txt"):
                with open("alerts.txt", "r") as f:
                    lines = f.readlines()
                with open("alerts.txt", "w") as f:
                    for line in lines:
                        if not line.startswith(f"{nt_id}|"):
                            f.write(line)

            self.list_timetable.controls.remove(cont)                

            await self.notifications.cancel(nt_id)
            print(f"Notification with ID {nt_id} cancelled.")
            self.page.update()
               
        except Exception as e:
            print(f"Error cancelling notification: {e}") 

    async def readtimetable(self):
            if os.path.exists("alerts.txt"):
                with open("alerts.txt", "r") as f:
                    lines = f.readlines()
                for line in lines:
                    nt_id_str, schld_time_str, subject, grade = line.strip().split("|")
                    nt_id = int(nt_id_str)
                    schld_time = datetime.fromisoformat(schld_time_str)

                    # Create a container for each saved class
                    container = ft.Container(
                        padding=ft.Padding.all(10),
                        margin=ft.Margin.all(5),
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment.TOP_LEFT,
                            end=ft.Alignment.BOTTOM_RIGHT,
                            colors=[ft.Colors.BLUE_900, ft.Colors.BLUE_300]
                        ),
                        border_radius=ft.BorderRadius.all(30),
                        content=ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text(f"Class: {grade}", size=15, weight=ft.FontWeight.BOLD),
                                        ft.Text(f"Subject: {subject}", size=15, weight=ft.FontWeight.NORMAL),
                                        ft.Text(f"Date: {schld_time.date()}", size=15, weight=ft.FontWeight.NORMAL),
                                        ft.Text(f"Time: {schld_time.time()}", size=15, weight=ft.FontWeight.NORMAL),
                                    ],
                                    expand=True,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Delete Entry",
                                    icon_color=ft.Colors.RED_400,
                                    # Use a closure to correctly reference nt_id and container
                                    on_click=lambda e, id=nt_id : asyncio.create_task(self.cancel_notification(id, cont=container))
                                )
                            ]
                        )
                    )

                    # Add the container to the timetable ListView
                    self.list_timetable.controls.append(container)

                # Update the page after loading all entries
                self.page.update()
                   

                
                    

def main(page: ft.Page):
    page.title = "Class Alert"
    ClassAlert(page)

ft.run(main)
