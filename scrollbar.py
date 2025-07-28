from tkinter import Canvas, Scrollbar, Frame as TkFrame

def with_scrollable_container(parent):
    outer_frame = TkFrame(parent)
    outer_frame.pack(fill="both", expand=True)

    canvas = Canvas(outer_frame, highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    scrollable_frame = TkFrame(canvas)
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas_frame = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

    def resize_canvas(event):
        canvas.itemconfig(canvas_frame, width=event.width)

    canvas.bind("<Configure>", resize_canvas)
    canvas.configure(yscrollcommand=scrollbar.set)

    return scrollable_frame
