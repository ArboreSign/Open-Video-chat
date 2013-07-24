#    This file is part of OpenVideoChat.
#
#    OpenVideoChat is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    OpenVideoChat is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with OpenVideoChat.  If not, see <http://www.gnu.org/licenses/>.
"""
:mod: `OpenVideoChat.activity/gui` -- Open Video Chat
=======================================================================

.. moduleauthor:: Justin Lewis <jlew.blackout@gmail.com>
.. moduleauthor:: Taylor Rose <tjr1351@rit.edu>
.. moduleauthor:: Fran Rogers <fran@dumetella.net>
.. moduleauthro:: Remy DeCausemaker <remyd@civx.us>
.. moduleauthor:: Caleb Coffie <CalebCoffie@gmail.com>
.. moduleauthor:: Casey DeLorme <cxd4280@rit.edu>
"""


# Imports
import logging
from gi.repository import Gtk
from gi.repository import Gdk
from gettext import gettext as _

# Testing GtkTreeIter with defined classes
from gi.repository.TelepathyGLib import Contact


# Define Logger for Logging & DEBUG level for Development
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Constants
MIN_CHAT_HEIGHT = 160
MAX_CHAT_MESSAGE_SIZE = 200


class Gui(Gtk.Grid):
    def __init__(self):
        Gtk.Grid.__init__(self, expand=True)
        logger.debug("Preparing GUI...")

        # Add Video
        self.attach(self.build_video(), 0, 1, 1, 1)

        # Add Chat
        self.attach(self.build_chat(), 0, 2, 1, 1)

        # Display Grid
        self.show()
        logger.debug("GUI Prepared")

    def build_video(self):
        logger.debug("Building Video...")

        # Create Video Component
        self.video = video = Gtk.DrawingArea(expand=True)
        video.override_background_color(Gtk.StateType.NORMAL, Gdk.RGBA(.01, .01, .01, .9))
        video.show()

        # Return Video Component
        logger.debug("Built Video")
        return video

    def build_chat(self):
        logger.debug("Building Chat...")

        # Create Chat Components
        self.chat_text_buffer = chat_text_buffer = Gtk.TextBuffer()
        chat_text_view = Gtk.TextView(editable=False, buffer=chat_text_buffer, cursor_visible=False, wrap_mode=Gtk.WrapMode.WORD)
        chat_scrollable_history = Gtk.ScrolledWindow(hexpand=True, hscrollbar_policy=Gtk.PolicyType.NEVER, vscrollbar_policy=Gtk.PolicyType.AUTOMATIC, min_content_height=MIN_CHAT_HEIGHT)
        chat_scrollable_history.add(chat_text_view)
        chat_entry = Gtk.Entry(hexpand=True, max_length=MAX_CHAT_MESSAGE_SIZE)
        chat_entry.connect("activate", self.send_message)
        chat_send_message_button = Gtk.Button(_("Send"))
        chat_send_message_button.connect("clicked", self.send_message)
        logger.debug("Built Chat Buffer, History, and Input")

        # Create Grid and Append Chat Components
        chat_grid = Gtk.Grid()
        chat_grid.attach(chat_scrollable_history, 0, 0, 2, 1)
        chat_grid.attach(chat_entry, 0, 1, 1, 1)
        chat_grid.attach(chat_send_message_button, 1, 1, 1, 1)
        logger.debug("Built Chat Grid")

        # Add Users List
        chat_grid.attach(self.build_user_list(), 2, 0, 1, 1)

        # Create Expander, Add Grid & Display
        chat_expander = Gtk.Expander(expanded=True, label=_("Chat"))
        chat_expander.add(chat_grid)
        chat_expander.show_all()
        logger.debug("Built Chat Expander")

        # Return Attachable Component
        logger.debug("Built Chat")
        return chat_expander

    def build_user_list(self):
        logger.debug("Building User List...")

        # Create Buffer for user storage
        self.user_list_store = Gtk.ListStore(str, Contact)

        # Create a Tree View and supply it the List Store
        user_list_tree_view = Gtk.TreeView(self.user_list_store)

        # Define the columns of the Tree View to render the data
        user_tree_view_column = Gtk.TreeViewColumn(
            "User Alias",            # Column Title (is displayed)
            Gtk.CellRendererText(),  # Renderer Component
            text=0                   # Column Index
        )

        # Sort by the alias column
        user_tree_view_column.set_sort_column_id(0)

        # Add the column to the Tree View
        user_list_tree_view.append_column(user_tree_view_column)

        # Create a scrollbox for user list
        user_list_scrolled_window = Gtk.ScrolledWindow(hscrollbar_policy=Gtk.PolicyType.NEVER, vscrollbar_policy=Gtk.PolicyType.AUTOMATIC, min_content_height=MIN_CHAT_HEIGHT)
        user_list_scrolled_window.add(user_list_tree_view)

        # Add a click handler to the tree view for user selection
        user_list_tree_view.connect('row-activated', self.user_selected)

        # Build Search Entry
        user_list_search_entry = Gtk.Entry(max_length=MAX_CHAT_MESSAGE_SIZE)
        user_list_search_entry.set_tooltip_text(_("Search for contacts..."))

        # Apply the search entry to the Tree View
        user_list_tree_view.set_search_entry(user_list_search_entry)

        # Define Storage Container & Attach Components
        user_list_grid = Gtk.Grid()
        user_list_grid.attach(user_list_scrolled_window, 0, 0, 1, 1)
        user_list_grid.attach(user_list_search_entry, 0, 1, 1, 1)

        # Create an expander to show the users on-demand & display all components
        user_list_expander = Gtk.Expander(label=_("Users"))
        user_list_expander.add(user_list_grid)
        user_list_expander.show_all()

        logger.debug("Built User List")

        # Return the top-level container
        return user_list_expander

    """ Network & User Methods """

    def add_a_contact(self, contact):
        # Simply add a user (logs would fill fast if I added one here)
        self.user_list_store.append([contact.get_alias(), contact])

    def user_selected(self, tree_view, selected_index, column_object):
        logger.debug("Identifying selected user to initiate communication...")

        # Can we pull the index from our List Store?
        # and Does it match when we sort?

        # First, can we access it via treeiter?
        print self.user_list_store[selected_index]

    """ Chat Methods """

    def send_message(self, sender):
        # Send a message over the tubes
        return False

    # def get_history(self):
    #     return self.chat_text.get_text(
    #             self.chat_text.get_start_iter(),
    #             self.chat_text.get_end_iter(),
    #             True)

    # def chat_write_line(self, line):
    #     self.chat_text.insert(self.chat_text.get_end_iter(), line, -1)

    # def receive_message(self, username, message):
    #     self.chat_text.insert(self.chat_text.get_end_iter(), "%s [%s]: %s\n" % (username, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message), -1)
    #     self.text_view.scroll_to_iter(self.chat_text.get_end_iter(), 0.1, False, 0.0, 0.0)

    # def send_message(self, sender):
    #     if self.chat_entry.get_text() != "":
    #         message = self.chat_entry.get_text()
    #         self.receive_message(self.network_stack.username, message)
    #         self.network_stack.send_message(message)
    #         self.chat_entry.set_text("")
    #         self.chat_entry.grab_focus()
