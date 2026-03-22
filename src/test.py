import flet as ft
from datetime import time


class ClassAlert:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.appbar = ft.AppBar(
            title=ft.Text("Class Alert", size=30, weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor=ft.Colors.BLUE_500,
        )

        def add_func(e):
            pass
        self.subject_name = ft.TextField(label="Subject Name", width=200)
        self.date = ft.Dropdown(
            label="Date",
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
        self.class_name = ft.TextField(label="Class Name", width=200)

        self.btntime = ft.Button(
            content=ft.Text("Pick Time"),
            on_click=lambda _: self.page.show_dialog(self.time_pick),
        )
                    

        self.addcontrols = ft.ListView(
            controls=[
                self.class_name,
                self.subject_name,
                self.date,
                self.btntime
            ],
            spacing=20,
            
        )


        self.add_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Add Lessons", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            content=ft.Container(
                content=self.addcontrols,
              ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: self.page.pop_dialog()),
                ft.TextButton("Add", on_click=lambda _: self.page.pop_dialog()),
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
                )
            ],
            expand=True,
        )

        self.page.add(
            ft.Row(
                controls=[self.container, self.list_timetable],
                alignment=ft.MainAxisAlignment.CENTER,
            )

        )

def main(page: ft.Page):
    page.title = "Class Alert"
    ClassAlert(page)

ft.run(main)
