# from venv import create
from guizero import *
import pyperclip
from widget_style1 import padding

# if widget being hovered is a button with image, it will change image to _hover version
# otherwise (its a button w/o image) so it will change bg and text colors
def hover(event_data):
    widget = event_data.widget
    if widget.image:
        widget.image = f"{widget.image[:-4]}_hover.png"
        if "home" not in widget.image:
            widget.height = widget.width = 25
        else:
            widget.height = 30
            widget.width = 75
    else:
        widget.bg = "white"
        widget.text_color = "#00467f"

# if its a button w/image - change to normal version of .png
# otherwise change the bg and text color back to normal (dark blue and white)
def normal_btn(event_data):
    widget = event_data.widget
    if widget.image:
        widget.image = f"{widget.image[:-10]}.png"
        if "home" in widget.image:
            widget.height = 30
            widget.width = 75
        else:
            widget.height = widget.width = 25
    else:
        widget.bg = "#00467f"
        widget.text_color = "white"

def switch_windows(tohide, toshow):
    tohide.hide()

    toshow.show()

# function that will erase the pre-existing content in a text box when textbox is clicked on
def erase_value(event_data):
    widget = event_data.widget
    widget.value = ""
    # set widget when clicked to nothing because you don't want user to click on the textbox while typing and lose all theyve typed
    widget.when_clicked = None
# SHOULD I STORE EACH RESPONSE AS A SEPARATE TXT FILE - TITLED THE SAME AS THE BUTTON IS TITLED? OR JUST HAVE ONE TXT ? I THINK ONE FOR EACH AT THIS POINT
def main():
    def copyto_clip(title, name_txtbox):
        usersname = name_txtbox.value
        # for title in resp_btns.keys():
        #     if button.text == title:
        # copy ticket response content to clipboard - will probably have to do some editing of this part of program - create some newlines/etc.
        # create string from content list
        content = resp_btns[title]["content"]
        new_string = ""
        for line in content:
            if "$ticketowner" in line:
                line_w_name = line.replace("$ticketowner", usersname)
            else:
                line_w_name = line
            new_string += f"{line_w_name}\n"
        pyperclip.copy(new_string)
        
        print('[**] DEBUG: Content copied.')
        # app.info('Content copied.')
    # this funciton will present user with the responses they have saved (it will actually present a window, which will have a textbox at the top to type a name, 
    # and then it will create a button for each response that the user has created. If the user clicks a button, it will copy the response to the user's clipboard 
    # WITH the name that the user typed into the top textbox inserted into the response. Then the user can just paste the response into OSTicket and reply quickly
    def show_view_responses():
        # hide main App
        app.hide()
        # reset resp_btns:
        # clear view_resp_mainbox
        # also need to print out resp_btns and resp_padding and see what they look like at this point of program
        for btn in resp_btns.keys():

            for widget in resp_btns[btn].keys():
                if widget != "content":
                    # right now i'm just try/catching the destroying of the buttons and padding - need to look into better way to do this
                    try:
                        
                        resp_btns[btn][widget].destroy()
                        resp_btns[btn][widget] = ""
                        # since the two dicts share the same string keys, can destroy the padding as well
                        # resp_padding[btn].destroy()

                    except ValueError:
                        print(f"Could not delete: {widget}")
                        pass
            try:
                resp_padding[btn].destroy()
                resp_padding[btn] = ""
            except ValueError:
                print(f"Could not delete: resp_padding {btn}")

        # show view resp window:
        windows["view"].show()
        for file in os.listdir("responses"):
            if ("response-" in file) and (file.endswith(".txt")):
                # that means its a response txt file, so open it, read it, and create the button from it
                with open(f"./responses/{file}", "r") as f:
                    lines = f.readlines()
                    # first line of each txt file will be button title/text
                    # also chop of \n with [:-1]
                    title = lines[0][:-1]
                    # each response-*.txt file will have a key in the resp_btns dict,
                    # whose value will be another dictionary, the 'btn' key holds the main button that user presses to copy ticket response
                    # 'content' holds the ticket response content
                    # 'box' holds the Box widget that holds all 3 buttons
                    # 'edit'/'delete' buttons to allow for edit/deletion of ticket response txt files
                    resp_btns[title] = {
                        # user clicks button to copy ticket response to clipboard
                        'btn': '',
                        # box which contains all other widgets in this dict - 'btn', 'edit', 'delete', etc.  
                        'box': '',
                        # edit button
                        'edit': '',
                        # delete response button which will delete the corresponding respone-*.txt file and update the GUI / destroy widgets
                        'delete': '', 
                        # padding between buttons:
                        'pad1': '', 
                        'pad2': '', 
                        'pad3': '',
                        # view button
                        'view':'',
                        # ticket response content which is copied to clipboard when 'btn' is clicked
                        'content': []
                    }
                    # dict - 'btn' key will hold button widget, and 'content' key will hold resp content from txt file
                    # 'box' - holds all other widgets in dictionary
                    resp_btns[title]['box'] = Box(view_resp_mainbox)

                    resp_btns[title]['btn'] = PushButton(resp_btns[title]['box'], text=title, width=20, align="left")

                    resp_padding[title] = Box(view_resp_mainbox, height=15, width="fill")
                    # from the 3rd line onwards will be the response content


                    # create edit button
                    resp_btns[title]['edit'] = PushButton(resp_btns[title]['box'], image="./img/edit.png", height=25, width=25, align="right")

                    # 'pad2' = padding in between edit and delete buttons
                    resp_btns[title]['pad2'] = Box(resp_btns[title]['box'], height="fill", width=15, align="right")

                    # create 'view' button to view the ticket response
                    resp_btns[title]['view'] = PushButton(resp_btns[title]['box'], image="./img/view.png", height=25, width=25, align="right")
                    resp_btns[title]['view'].update_command(view_current_response, args=[title])

                    # add space between the view and delete buttons
                    resp_btns[title]['pad3'] = Box(resp_btns[title]['box'], height="fill", width=15, align="right")

                    # put delete button next to edit button:
                    resp_btns[title]['delete'] = PushButton(resp_btns[title]['box'], image="./img/trash.png", height=25, width=25, align="right")
                    # assign command to delete buttons
                    resp_btns[title]['delete'].update_command(delete_response, args=[title])


                    # 'pad1' key is the padding to the right of the main button (resp_btns[title]['btn'])
                    resp_btns[title]['pad1'] = Box(resp_btns[title]['box'], height="fill", width=20, align="right")
                    # skip the first two lines of the txt file - first line contains the title, and the second line is blank
                    for line in lines[2:]:
                        resp_btns[title]['content'].append(line)
                    # assign command to button:
                    resp_btns[title]['btn'].update_command(copyto_clip, args=[title, name_txtbox])

                    resp_btns[title]['btn'].bg = "#00467f"
                    resp_btns[title]['btn'].text_color = "white"
                    # make cursor a target when hovering on the buttons
                    resp_btns[title]['btn'].tk.config(cursor="target")

                    # set common properties of buttons in resp_btns[title].keys()
                    for key in resp_btns[title].keys():
                        resp_btns[title][key].when_mouse_enters = hover
                        resp_btns[title][key].when_mouse_leaves = normal_btn

                # close file
                f.close()

    def view_current_response(title):
        # need to clean up this output / maybe do it differently
        app.info("Selected response: ", f"{resp_btns[title]['content']}")


    # function will create a 'response-*.txt' file using title / content values entered by user on the add response window
    def create_response(title, response_content):
        # since the widgets are transferred in as parameters, I need to take the value/text to get current text in them
        title = title.value
        response_content = response_content.value
        with open(f"./responses/response-{title}.txt", "w") as txtfile:
            txtfile.write(f"{title}\n\n")
            txtfile.writelines(response_content)

        # notify user that text file has been created, reset the erase_value when clicked event
        add_resp_txtbox.value = f"[+] ./responses/response-{title}.txt created"
        # add_resp_txtbox.when_clicked = erase_value
        app.after(1500, switch_windows, args=[windows["add"], app])

    # this function just reloads the view responses Window
    def update_view_responses():
        reg_buttons["view"].update_command(show_view_responses)
        app.after(1, show_view_responses)

    def delete_response(response_title):
        # all I need to do is delete the txt file, then call the update function and everything else will update itself based on the response-*.txt files in the directory
        os.remove(f"./responses/response-{response_title}.txt")
        resp_btns[response_title]
        update_view_responses()

    # 'refresh' app - just rebuilds the app, this has to be kept in because of menubar - can i add arguments to function in menubar?
    def refresh_app():
        app.destroy()
        main()

    def show_stored_greetings():
        pass


    ##### Widget Storage (mostly) Dictionaries  #####
    # dictionary to hold regular buttons (buttons w/no images that have dark blue bg and white text color)
    reg_buttons = {}
    # Window widgets - view responses window, add response window...
    windows = {}

    # holds response buttons on the view responses Window - this dictionary's keys will be generated from the 'response-*.txt' files in the responses directory each time the view responses window is shown
    resp_btns = {}
    # each filename key of resp_btns will have a dictionary as a value - this inner dictionary will have values corresponding to various widgets that will be created for each stored response i.e. response-*.txt file
    
    # holds the Boxs (padding) that go below each resp_btn on the view reponses Window:
    resp_padding = {}


    app = App(title="Ticket Responses", height=250, width=600, bg="#01a161")
    # define font for App - Roboto like dtcc.edu
    app.font = "Roboto"

    # add basic menubar (need to edit this)
    menubar = MenuBar(app,
                  toplevel=["File", "Edit"],
                  options=[
                      [ ["Refresh", refresh_app],["Exit", exit]],
                      # option to show the default greetings window which will let user edit their stored greetings
                      # there will be a stored greetings dropdown menu so user can select desired stored greeting to add to beginning of ticket response
                      [["Stored Greetings", show_stored_greetings]]
                  ])


    ##### Define VIEW RESPONSES Window and static contents   #####
    windows["view"] = Window(app, title="View Ticket Responses", bg="#01a161", height=600, width=400)

    # add title / other static widgets inside view resp window:
    Box(windows["view"], height=15, width="fill", align="top")

    # title for 'view' Window can be a Text widget or the Picture widget
    # view_title = Text(windows["view"], text="Click a response button to \ncopy response to clipboard", align="top", size=16)
    view_title = Picture(windows["view"], image="./img/clicktocopy.png", height=50, width=200, align="top")

    # textbox to type users name (with Box s for padding/container)
    txtbox_container = Box(windows["view"], height=40, width="fill")

    # use padding class to create the 4 Box widgets for padding
    padding(txtbox_container, 10, 10, 10, 0)

    name_txtbox = TextBox(txtbox_container, text="Enter user's name here then click a button", width=35)
    name_txtbox.bg = "#EAFEF1"
    name_txtbox.text_color = "black"
    name_txtbox.when_clicked = erase_value
    # will hold the response buttons that are generated from the response-*.txt files in the 'responses' directory
    view_resp_mainbox = Box(windows["view"])


    ##### Define ADD RESPONSE Window and contents (they're all)   #####
    windows["add"] = Window(app, title="Add Ticket Response", bg="#01a161", height=600)
    Box(windows["add"], height=25, width="fill", align="top")

    # box to hold text and textbox widget - to enter button/response title:
    add_title_box = Box(windows["add"], height=20, width="fill", align="top")
    Box(add_title_box, height="fill", width=30, align="left")
    add_title_txtbox = TextBox(add_title_box, text="Enter response title", align="left", width=60)
    add_title_txtbox.bg = "#EAFEF1"
    # add_title_txtbox.text_color = "white"

    # box where user types response:
    add_resp_box = Box(windows["add"], height=400, width="fill", align="top")

    # use padding class to create the 4 Box widgets for padding
    padding(add_resp_box, 15, 15, 10, 10)

    add_resp_txtbox = TextBox(add_resp_box, height="fill", width=65, text="Please use $ticketowner in place of ticket owner (user's) name.", multiline=True, scrollbar=True)
    add_resp_txtbox.bg = "#EAFEF1"

    # add submit new reponse button to bottom the add response Window
    add_resp_btm_box = Box(windows["add"], height=50, width="fill")
    reg_buttons["create"] = PushButton(add_resp_btm_box, text="Create response", height=25, width=40)
    padding(add_resp_btm_box, 0, 0, 10, 10)

    btm_btns = {}
    # add a 'return' button to both windows that will return to main App (i.e. hide the window then show the App)
    for window in windows.keys():
        btm_btns[window] = {}
        # add bottom boxes, hide Windows
        Box(windows[window], height=15, width="fill", align="top")
        windows[window].hide()

        # add simple menubar to each Window w/exit button and button to refresh app
        MenuBar(windows[window],
                toplevel=["File"],
                options=[
                    [ ["Refresh", refresh_app],["Exit", exit]]
                ])
        # create box to hold the Home and refresh buttons:
        btm_box = Box(windows[window], height=50, width="fill", align="bottom")
        padding(btm_box, 10, 10, 0, 5)

        btm_btns[window]["home"] = PushButton(btm_box, image="./img/home.png", align="left", padx=10, pady=10, height=30, width=75)
        btm_btns[window]["refresh"] = PushButton(btm_box, image="./img/refresh.png", align="right", height=25, width=25)
        for thewindow in btm_btns.keys():
            for btn in btm_btns[thewindow].keys():
                btm_btns[thewindow][btn].when_mouse_enters = hover
                btm_btns[thewindow][btn].when_mouse_leaves = normal_btn
                btm_btns[thewindow][btn].bg = "#00467f"
                btm_btns[thewindow][btn].text_color = "white"

        # new_button.update_command(return_home, args=[windows[window], app])
        btm_btns[window]["home"].update_command(switch_windows, args=[windows[window], app])
        # switching back to the App/main window will effectively 'refresh' since when user goes back to view responses page it will recreate buttons from the response-*.txt files
        btm_btns[window]["refresh"].update_command(switch_windows, args=[windows[window], app])

        # make cursor - exchange
        btm_btns[window]["refresh"].tk.config(cursor="exchange")
    # add space between top of window and title
    Box(app, height=20, width="fill", align="top")

    title = Text(app, text="Ticket Responses", align="top", size=20)
    title.text_color = "white"

    # box to add some space between the title and the two buttons
    Box(app, height=30, width="fill", align="top")

    button_box = Box(app, width="fill", align="top")
    Box(button_box, height="fill", width=100)
    Box(button_box, align="left", height="fill", width=150)
    reg_buttons["view"] = PushButton(button_box, text="View Responses", align="left", width=15)

    Box(button_box, align="right", height="fill", width=150)
    reg_buttons["add"] = PushButton(button_box, text="Add Response", align="right", width=15)

    # set reg_buttons settings - dark blue bg, white text color, roboto font etc.
    for button in reg_buttons.keys():
        # use full_button class to style buttons the same way
        reg_buttons[button].bg = "#00467f"
        reg_buttons[button].text_color = "white"
        reg_buttons[button].when_mouse_enters = hover
        reg_buttons[button].when_mouse_leaves = normal_btn

    add_title_txtbox.when_clicked = erase_value
    add_resp_txtbox.when_clicked = erase_value
    # assign functions to buttons:
    reg_buttons["view"].update_command(update_view_responses)
    # reg_buttons["add"].update_command(show_add_response, args=[windows["add"], app])
    reg_buttons["add"].update_command(switch_windows, args=[app, windows["add"]])
    reg_buttons["create"].update_command(create_response, args=[add_title_txtbox, add_resp_txtbox])

    # create page where user can view/edit stored greetings


    app.display()


if __name__ == "__main__":
    main()