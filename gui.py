#!/usr/bin/python
from Tkinter import *

import socket
import math

class Application(Frame):
    """ {Application}: is the container for the widgets and I/O sockets."""

    def __init__(self, master = None):
	""" {Applicaiton}: Initialize {self}. """

	# Initialize the GUI:
        Frame.__init__(self, master)
        self.grid()
        self.widgets_create()

	# Pi is a useful constant for radians <=> degrees conversion:
	self.pi = 3.14159265358979323846

	# Connect to Host_Control server:
	host = "192.168.1.5"
	port = 6543
	host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host_socket.connect((host, port))
	self.host_socket = host_socket

	# Bind an event handler for reading data from {host_socket}:
	self.tk.createfilehandler(host_socket, tkinter.READABLE, self.host_read)

	# Latest camera values:
	self.camera_bearing = 0.0
	self.camera_x = 0.0
	self.camera_y = 0.0
	# Anchor ddB/X/Y values:
	self.addb = 0.0
	self.addx = 0.0
	self.addy = 0.0
	# Positive ddB/X/Y values:
	self.pddb = 0.0
	self.pddx = 0.0
	self.pddy = 0.0
	# Negative ddB/X/Y values:
	self.nddb = 0.0
	self.nddx = 0.0
	self.nddy = 0.0

    def widgets_create(self):
	""" {Application}: Create the widges for {self}. """

	# Create the [Camera On] button:
	camera_on_button = Button(self, \
	  text = "Camera On", command = self.camera_on)
	self.camera_on_button = camera_on_button

	# Create the [Camera Off] button:
	camera_off_button = \
	  Button(self, text = "Camera Off", command = self.camera_off)
	self.camera_off_button = camera_off_button

	# Create the [Camera Sync] button:
	camera_sync_button = Button(self, \
	  text = "Camera Sync", command = self.camera_sync)
	self.camera_sync_button = camera_sync_button

	# Create the [Show] button:
	show_button = Button(self, text = "Show", command = self.show)
	self.show_button = show_button

	# Create the [Clear] button:
	clear_button = Button(self, text = "Clear", command = self.clear)

	# Create the [Save] button:
	save_button = Button(self, text = "Save", command = self.save)
	self.save_button = save_button

	# Create the [Way Delete] button:
	way_delete_button = Button(self, text = "Way Delete", \
	  state = DISABLED, command = self.way_delete)
	self.way_delete_button = way_delete_button

	# Create the [Way Create] button:
	way_create_button = Button(self, text = "Way Create", \
	  state = DISABLED, command = self.way_create)
	self.way_create_button = way_create_button

	# Create the [Way Go To] button:
	way_goto_button = Button(self, text = "Way Go To", \
	  state = DISABLED, command = self.way_goto)
	self.way_goto_button = way_goto_button

	# Create the [Halt] button:
	halt_button = Button(self, text = "Halt", command = self.halt)
	self.halt = halt_button

	# Create the [Go To] check button:
	self.goto_value = BooleanVar()
	goto_button = Checkbutton(self, text = "Go To", \
	  variable = self.goto_value, onvalue = True, offvalue = False,
	  command = self.goto)
	self.goto_button = goto_button

	# Create the [Way_Update] constants button:
	way_update_button = \
	  Button(self, text = "Way Update", command = self.way_update)
	self.way_update_button = way_update_button

	# Create the [Const Update] button:
	constants_update_button = Button(self,
	  text = "Const Update", command = self.constants_update)
	self.constants_update_button = constants_update_button

	# Create the [Grip] button:
	grip_button = Button(self, text = "Grab", command = self.grip)
	self.grip_button = grip_button

        # Create the [Release] button:
	release_button = Button(self, \
	  text = "Release", command = self.release)
	self.release_button = release_button

        # Create the [Way Grab] button:
	way_grab_button = Button(self, text = "Way Grab", \
	  state = DISABLED, command = self.way_grab)
	self.way_grab_button = way_grab_button

        # Create the [Way Release] button:
	way_release_button = Button(self, text = "Way Release", \
	  state = DISABLED, command = self.way_release)
	self.way_release_button = way_release_button

	# Create the [Move] button:
	move_button = Button(self, text = "Move", \
	  state = DISABLED, command = self.move)
	self.move_button = move_button

	# Create the [UnMove] button:
	unmove_button = Button(self, text = "UnMove", \
	  state = DISABLED, command = self.unmove)
	self.unmove_button = unmove_button

	# Create the map canvas:
	height = 500
	width = 800
	canvas = Canvas(self, bg="white", height = height, width = width)
	map_canvas = Map_Canvas(canvas, width, height, self)
	self.map_canvas = map_canvas

	# Create the motor stall label:
	motor_stall_label = Label(self, text = "Motor Stall:")
	self.motor_stall_label = motor_stall_label

	# Create the motor stall entry:
	motor_stall_entry = Entry(self, width = 5, background = "white")
	self.motor_stall_entry = motor_stall_entry

	# Create the speed limit label:
	speed_limit_label = Label(self, text = "Speed Limit:")
	self.speed_limit_label = speed_limit_label

	# Create the speed limit entry:
	speed_limit_entry = Entry(self, width = 5, background = "white")
	self.speed_limit_entry = speed_limit_entry

	# Create the twist limit label:
	twist_limit_label = Label(self, text = "Twist Limit:")
	self.twist_limit_label = twist_limit_label

	# Create the twist limit entry:
	twist_limit_entry = Entry(self, width = 5, background = "white")
	self.twist_limit_entry = twist_limit_entry

	# Create the bearing limit label:
	bearing_limit_label = Label(self, text = "Bearing Limit:")
	self.bearing_limit_label = bearing_limit_label

	# Create the bearing limit entry:
	bearing_limit_entry = Entry(self, width = 5, background = "white")
	self.bearing_limit_entry = bearing_limit_entry

	# Create the target limit label:
	target_limit_label = Label(self, text = "Target Limit:")
	self.target_limit_label = target_limit_label

	# Create the target limit entry:
	target_limit_entry = Entry(self, width = 5, background = "white")
	self.target_limit_entry = target_limit_entry

	# Create the PID_P label:
	pid_p_label = Label(self, text = "PID_P:")
	self.pid_p_label = pid_p_label

	# Create the PID P(roportional) entry:
	pid_p_entry = Entry(self, width = 5, background = "white")
	self.pid_p_entry = pid_p_entry

	# Create the PID I(ntegral) label:
	pid_i_label = Label(self, text = "PID_I:")
	self.pid_i_label = pid_i_label

	# Create the PID I(ntegeral) entry:
	pid_i_entry = Entry(self, width = 5, background = "white")
	self.pid_i_entry = pid_i_entry

	# Create the PID D(ifferential) label:
	pid_d_label = Label(self, text = "PID_D:")
	self.pid_d_label = pid_d_label

	# Create the PID D(ifferential) entry:
	pid_d_entry = Entry(self, width = 5, background = "white")
	self.pid_d_entry = pid_d_entry

	# Create the Linear coefficient label:
	linear_label = Label(self, text = "Linear:")
	self.linear_label = linear_label

	# Create the Linear coefficient entry:
	linear_entry = Entry(self, width = 5, background = "white")
	self.linear_entry = linear_entry

	# Create the ramp label:
	ramp_label = Label(self, text = "Ramp:")
	self.ramp_label = ramp_label

	# Create the ramp entry:
	ramp_entry = Entry(self, width = 5, background = "white")
	self.ramp_entry = ramp_entry

	# Create the camera_dx label:
	camera_dx_label = Label(self, text = "Camera DX:")
	self.camera_dx_label = camera_dx_label

	# Create the camera_dx entry:
	camera_dx_entry = Entry(self, width = 5, background = "white")
	self.camera_dx_entry = camera_dx_entry

	# Create the camera_dy label:
	camera_dy_label = Label(self, text = "Camera DY:")
	self.camera_dy_label = camera_dy_label

	# Create the camera_dy entry:
	camera_dy_entry = Entry(self, width = 5, background = "white")
	self.camera_dy_entry = camera_dy_entry

	# Create the camera_twist label:
	camera_twist_label = Label(self, text = "Camera Twist:")
	self.camera_twist_label = camera_twist_label

	# Create the camera_twist entry:
	camera_twist_entry = Entry(self, width = 5, background = "white")
	self.camera_twist_entry = camera_twist_entry

	# Create the Grip_P label:
	grip_p_label = Label(self, text = "Grip_P:")
	self.grip_p_label = grip_p_label

	# Create the Grip P(roportional) entry:
	grip_p_entry = Entry(self, width = 5, background = "white")
	self.grip_p_entry = grip_p_entry

	# Create the Grip I(ntegral) label:
	grip_i_label = Label(self, text = "Grip_I:")
	self.grip_i_label = grip_i_label

	# Create the Grip I(ntegeral) entry:
	grip_i_entry = Entry(self, width = 5, background = "white")
	self.grip_i_entry = grip_i_entry

	# Create the Grip D(ifferential) label:
	grip_d_label = Label(self, text = "Grip_D:")
	self.grip_d_label = grip_d_label

	# Create the Grip D(ifferential) entry:
	grip_d_entry = Entry(self, width = 5, background = "white")
	self.grip_d_entry = grip_d_entry

	# Create the dead reckoning X label:
	reckon_x_label = Label(self, text = "Reckon X:")
	self.reckon_x_label = reckon_x_label

	# Create the reckon X entry:
	reckon_x_entry = Entry(self, width = 5, background = "white")
	self.reckon_x_entry = reckon_x_entry

	# Create the reckon Y label:
	reckon_y_label = Label(self, text = "Reckon Y:")
	self.reckon_y_label = reckon_y_label

	# Create the reckon Y entry:
	reckon_y_entry = Entry(self, width = 5, background = "white")
	self.reckon_y_entry = reckon_y_entry

	# Create the reckon bearing label:
	reckon_bearing_label = Label(self, text = "Reckon Bearing:")
	self.reckon_bearing_label = reckon_bearing_label

	# Create the reckon bearing entry:
	reckon_bearing_entry = Entry(self, width = 5, background = "white")
	self.reckon_bearing_entry = reckon_bearing_entry

	# Create the target bearing label:
	target_bearing_label = Label(self, text = "Target Bearing:")
	self.target_bearing_label = target_bearing_label

	# Create the target bearing entry:
	target_bearing_entry = Entry(self, width = 5, background = "white")
	self.target_bearing_entry = target_bearing_entry

	# Create the target distance label:
	target_distance_label = Label(self, text = "Target Distance:")
	self.target_distance_label = target_distance_label

	# Create the target distance entry:
	target_distance_entry = Entry(self, width = 5, background = "white")
	self.target_distance_entry = target_distance_entry

	# Create the way flags label:
	way_flags_label = Label(self, text = "Way Flags:")
	self.way_flags_label = way_flags_label

	# Create the way flags entry:
	way_flags_entry = Entry(self, width = 5, background = "white")
	self.way_flags_entry = way_flags_entry

	# Create the way height label:
	way_height_label = Label(self, text = "Way Height:")
	self.way_height_label = way_height_label

	# Create the way height entry:
	way_height_entry = Entry(self, width = 5, background = "white")
	self.way_height_entry = way_height_entry

	# Create the way open width label:
	way_open_width_label = Label(self, text = "Way Open Width:")
	self.way_open_width_label = way_open_width_label

	# Create the way open width entry:
	way_open_width_entry = Entry(self, width = 5, background = "white")
	self.way_open_width_entry = way_open_width_entry

	# Create the way close width label:
	way_close_width_label = Label(self, text = "Way Close Width:")
	self.way_close_width_label = way_close_width_label

	# Create the way close width entry:
	way_close_width_entry = Entry(self, width = 5, background = "white")
	self.way_close_width_entry = way_close_width_entry

	# Create the way name label:
	way_name_label = Label(self, text = "Way Name:")
	self.way_name_label = way_name_label

	# Create the way name entry:
	way_name_entry = Entry(self,  width = 8, background = "white")
	self.way_name_entry = way_name_entry

	# Create the left force label:
	left_force_label = Label(self, text = "Left Force:")
	self.left_force_label = left_force_label

	# Create the left force entry:
	left_force_entry = Entry(self,  width = 5, background = "white")
	self.left_force_entry = left_force_entry

	# Create the right force label:
	right_force_label = Label(self, text = "Right Force:")
	self.right_force_label = right_force_label

	# Create the right force entry:
	right_force_entry = Entry(self,  width = 5, background = "white")
	self.right_force_entry = right_force_entry

	# Create the fiducial X label:
	fiducial_x_label = Label(self, text = "Fiducial X:")
	self.fiducial_x_label = fiducial_x_label

	# Create the fiducial X entry:
	fiducial_x_entry = Entry(self, width = 5, background = "white")
	self.fiducial_x_entry = fiducial_x_entry

	# Create the fiducial Y label:
	fiducial_y_label = Label(self, text = "Fiducial Y:")
	self.ficucial_y_label = fiducial_y_label

	# Create the fiducial Y entry:
	fiducial_y_entry = Entry(self, width = 5, background = "white")
	self.fiducial_y_entry = fiducial_y_entry

	# Create the fiducial bearing label:
	fiducial_bearing_label = Label(self, text = "Fiducial Bearing:")
	self.fiducal_bearing_label = fiducial_bearing_label

	# Create the fiducial bearing entry:
	fiducial_bearing_entry = \
	  Entry(self, width = 5, background = "white")
	self.fiducial_bearing_entry = fiducial_bearing_entry

	# Create the fiducial tag label:
	fiducial_tag_label = Label(self, text = "Fiducial Tag:")
	self.fiducal_tag_label = fiducial_tag_label

	# Create the fiducial tag entry:
	fiducial_tag_entry = \
	  Entry(self, width = 5, background = "white")
	self.fiducial_tag_entry = fiducial_tag_entry

	# Create the fiducial tag entry:
	fiducial_edge_entry = \
	  Entry(self, width = 8, background = "white")
	self.fiducial_edge_entry = fiducial_edge_entry

	# Create the fiducial tag label:
	fiducial_edge_label = Label(self, text = "Fiducial Edge:")
	self.fiducal_edge_label = fiducial_edge_label

	# Create the tag X label:
	tag_x_label = Label(self, text = "Tag X:")
	self.tag_x_label = tag_x_label

	# Create the tag X entry:
	tag_x_entry = Entry(self, width = 5, background = "white")
	self.tag_x_entry = tag_x_entry

	# Create the tag Y label:
	tag_y_label = Label(self, text = "Tag Y:")
	self.tag_y_label = tag_y_label

	# Create the tag Y entry:
	tag_y_entry = Entry(self, width = 5, background = "white")
	self.tag_y_entry = tag_y_entry

	# Create the tag dX label:
	tag_dx_label = Label(self, text = "Tag dX:")
	self.tag_dx_label = tag_dx_label

	# Create the tag dX entry:
	tag_dx_entry = Entry(self, width = 5, background = "white")
	self.tag_dx_entry = tag_dx_entry

	# Create the tag dY label:
	tag_dy_label = Label(self, text = "Tag dY:")
	self.tag_dy_label = tag_dy_label

	# Create the tag dY entry:
	tag_dy_entry = Entry(self, width = 5, background = "white")
	self.tag_dy_entry = tag_dy_entry

	# Create the tag distance label:
	tag_distance_label = Label(self, text = "Tag Distance:")
	self.tag_distance_label = tag_distance_label

	# Create the tag distance entry:
	tag_distance_entry = Entry(self, width = 5, background = "white")
	self.tag_distance_entry = tag_distance_entry


	# Create the tag positive ddB label:
	tag_pddb_label = Label(self, text = "Positive ddB:")
	self.tag_pddb_label = tag_pddb_label

	# Create the tag positive ddB entry:
	tag_pddb_entry = Entry(self, width = 5, background = "white")
	self.tag_pddb_entry = tag_pddb_entry

	# Create the tag positive ddX label:
	tag_pddx_label = Label(self, text = "Positive ddX:")
	self.tag_pddx_label = tag_pddx_label

	# Create the tag positive ddX entry:
	tag_pddx_entry = Entry(self, width = 5, background = "white")
	self.tag_pddx_entry = tag_pddx_entry

	# Create the tag positive ddY label:
	tag_pddy_label = Label(self, text = "Positive ddY:")
	self.tag_pddy_label = tag_pddy_label

	# Create the tag positive ddY entry:
	tag_pddy_entry = Entry(self, width = 5, background = "white")
	self.tag_pddy_entry = tag_pddy_entry

	# Create the tag negative ddB label:
	tag_nddb_label = Label(self, text = "Negative ddB:")
	self.tag_nddb_label = tag_nddb_label

	# Create the tag negative ddB entry:
	tag_nddb_entry = Entry(self, width = 5, background = "white")
	self.tag_nddb_entry = tag_nddb_entry

	# Create the tag negative ddX label:
	tag_nddx_label = Label(self, text = "Negative ddX:")
	self.tag_nddx_label = tag_nddx_label

	# Create the tag negative ddX entry:
	tag_nddx_entry = Entry(self, width = 5, background = "white")
	self.tag_nddx_entry = tag_nddx_entry

	# Create the tag negative ddY label:
	tag_nddy_label = Label(self, text = "Negative ddY:")
	self.tag_nddy_label = tag_nddy_label

	# Create the tag negative ddY entry:
	tag_nddy_entry = Entry(self, width = 5, background = "white")
	self.tag_nddy_entry = tag_nddy_entry

	# Create the [Clear +/- ddX/Y] constants button:
	clear_pnddbxy_button = Button(self, text = "Clear +/- ddB/X/Y", \
	  command = self.clear_pnddbxy)
	self.clear_pnddbxy_button = clear_pnddbxy_button


	# Create the tag anchor ddB label:
	tag_addb_label = Label(self, text = "Anchor ddB:")
	self.tag_addb_label = tag_addb_label

	# Create the tag anchor ddB entry:
	tag_addb_entry = Entry(self, width = 5, background = "white")
	self.tag_addb_entry = tag_addb_entry

	# Create the tag anchor ddX label:
	tag_addx_label = Label(self, text = "Anchor ddX:")
	self.tag_addx_label = tag_addx_label

	# Create the tag anchor ddX entry:
	tag_addx_entry = Entry(self, width = 5, background = "white")
	self.tag_addx_entry = tag_addx_entry

	# Create the tag anchor ddY label:
	tag_addy_label = Label(self, text = "Anchor ddY:")
	self.tag_addy_label = tag_addy_label

	# Create the tag anchor ddY entry:
	tag_addy_entry = Entry(self, width = 5, background = "white")
	self.tag_addy_entry = tag_addy_entry

	# Create the [Clear +/- ddX/Y] constants button:
	clear_pnddbxy_button = Button(self, text = "Clear +/- ddB/X/Y", \
	  command = self.clear_pnddbxy)
	self.clear_pnddbxy_button = clear_pnddbxy_button

	# Grid the GUI items up:
	ctl1_row = 0
	camera_on_button.grid(row = ctl1_row, column = 0)
	camera_off_button.grid(row = ctl1_row, column = 1)
	camera_sync_button.grid(row = ctl1_row, column = 2)
	constants_update_button.grid(row = ctl1_row, column = 3)
	way_update_button.grid(row = ctl1_row, column = 4)
	grip_button.grid(row = ctl1_row, column = 5)
	release_button.grid(row = ctl1_row, column = 6)
	save_button.grid(row = ctl1_row, column = 7)
	clear_button.grid(row = ctl1_row, column = 8)
	show_button.grid(row = ctl1_row, column = 9)

	ctl2_row = ctl1_row + 1
	way_delete_button.grid(row = ctl2_row, column = 0)
	way_create_button.grid(row = ctl2_row, column = 1)
	way_goto_button.grid(row = ctl2_row, column = 2)
	goto_button.grid(row = ctl2_row, column = 3)
	halt_button.grid(row = ctl2_row, column = 4)
	way_grab_button.grid(row = ctl2_row, column = 5)
	way_release_button.grid(row = ctl2_row, column = 6)
	move_button.grid(row = ctl2_row, column = 7)
	unmove_button.grid(row = ctl2_row, column = 8)

	canvas_row = ctl2_row + 1
	canvas.grid(row = canvas_row, column = 0, columnspan = 10)

	tag_row = canvas_row + 1
	tag_x_label.grid(row = tag_row, column = 0, sticky = E)
	tag_x_entry.grid(row = tag_row, column = 1, sticky = W)
	tag_y_label.grid(row = tag_row, column = 2, sticky = E)
	tag_y_entry.grid(row = tag_row, column = 3, sticky = W)
	tag_dx_label.grid(row = tag_row, column = 4, sticky = E)
	tag_dx_entry.grid(row = tag_row, column = 5, sticky = W)
	tag_dy_label.grid(row = tag_row, column = 6, sticky = E)
	tag_dy_entry.grid(row = tag_row, column = 7, sticky = W)
	tag_distance_label.grid(row = tag_row, column = 8, sticky = E)
	tag_distance_entry.grid(row = tag_row, column = 9, sticky = W)

	reck_row = tag_row + 1
	reckon_bearing_label.grid(row = reck_row, column = 0, sticky = E)
	reckon_bearing_entry.grid(row = reck_row, column = 1, sticky = W)
	reckon_x_label.grid(row = reck_row, column = 2, sticky = E)
	reckon_x_entry.grid(row = reck_row, column = 3, sticky = W)
	reckon_y_label.grid(row = reck_row, column = 4, sticky = E)
	reckon_y_entry.grid(row = reck_row, column = 5, sticky = W)
	target_bearing_label.grid(row = reck_row, column = 6, sticky = E)
	target_bearing_entry.grid(row = reck_row, column = 7, sticky = W)
	target_distance_label.grid(row = reck_row, column = 8, sticky = E)
	target_distance_entry.grid(row = reck_row, column = 9, sticky = W)

	way_row1 = reck_row + 1
	way_flags_label.grid(row = way_row1, column = 0, sticky = E)
	way_flags_entry.grid(row = way_row1, column = 1, sticky = W)
	way_height_label.grid(row = way_row1, column = 2, sticky = E)
	way_height_entry.grid(row = way_row1, column = 3, sticky = W)
	way_open_width_label.grid(row = way_row1, column = 4, sticky = E)
	way_open_width_entry.grid(row = way_row1, column = 5, sticky = W)
	way_close_width_label.grid(row = way_row1, column = 6, sticky = E)
	way_close_width_entry.grid(row = way_row1, column = 7, sticky = W)
	way_name_label.grid(row = way_row1, column = 8, sticky = E)
	way_name_entry.grid(row = way_row1, column = 9, sticky = W)

	k0_row = way_row1 + 1
	motor_stall_label.grid(row = k0_row, column = 0, sticky = E)
	motor_stall_entry.grid(row = k0_row, column = 1, sticky = W)
	speed_limit_label.grid(row = k0_row, column = 2, sticky = E)
	speed_limit_entry.grid(row = k0_row, column = 3, sticky = W)
	twist_limit_label.grid(row = k0_row, column = 4, sticky = E)
	twist_limit_entry.grid(row = k0_row, column = 5, sticky = W)
	bearing_limit_label.grid(row = k0_row, column = 6, sticky = E)
	bearing_limit_entry.grid(row = k0_row, column = 7, sticky = W)
	target_limit_label.grid(row = k0_row, column = 8, sticky = E)
	target_limit_entry.grid(row = k0_row, column = 9, sticky = W)

	k1_row = k0_row + 1
	pid_p_label.grid(row = k1_row, column = 0, sticky = E)
	pid_p_entry.grid(row = k1_row, column = 1, sticky = W)
	pid_i_label.grid(row = k1_row, column = 2, sticky = E)
	pid_i_entry.grid(row = k1_row, column = 3, sticky = W)
	pid_d_label.grid(row = k1_row, column = 4, sticky = E)
	pid_d_entry.grid(row = k1_row, column = 5, sticky = W)
	ramp_label.grid(row = k1_row, column = 6, sticky = E)
	ramp_entry.grid(row = k1_row, column = 7, sticky = W)
	linear_label.grid(row = k1_row, column = 8, sticky = E)
	linear_entry.grid(row = k1_row, column = 9, sticky = W)

	k2_row = k1_row + 1
	left_force_label.grid(row = k2_row, column = 0, sticky = E)
	left_force_entry.grid(row = k2_row, column = 1, sticky = W)
	right_force_label.grid(row = k2_row, column = 2, sticky = E)
	right_force_entry.grid(row = k2_row, column = 3, sticky = W)
	grip_p_label.grid(row = k2_row, column = 4, sticky = E)
	grip_p_entry.grid(row = k2_row, column = 5, sticky = W)
	grip_i_label.grid(row = k2_row, column = 6, sticky = E)
	grip_i_entry.grid(row = k2_row, column = 7, sticky = W)
	grip_d_label.grid(row = k2_row, column = 8, sticky = E)
	grip_d_entry.grid(row = k2_row, column = 9, sticky = W)

	k3_row = k2_row + 1
	camera_dx_label.grid(row = k3_row, column = 0, sticky = E)
	camera_dx_entry.grid(row = k3_row, column = 1, sticky = W)
	camera_dy_label.grid(row = k3_row, column = 2, sticky = E)
	camera_dy_entry.grid(row = k3_row, column = 3, sticky = W)
	camera_twist_label.grid(row = k3_row, column = 4, sticky = E)
	camera_twist_entry.grid(row = k3_row, column = 5, sticky = W)

	fid_row = k3_row + 1
	fiducial_tag_label.grid(row = fid_row, column = 0, sticky = E)
	fiducial_tag_entry.grid(row = fid_row, column = 1, sticky = W)
	fiducial_x_label.grid(row = fid_row, column = 2, sticky = E)
	fiducial_x_entry.grid(row = fid_row, column = 3, sticky = W)
	fiducial_y_label.grid(row = fid_row, column = 4, sticky = E)
	fiducial_y_entry.grid(row = fid_row, column = 5, sticky = W)
	fiducial_bearing_label.grid(row = fid_row, column = 6, sticky = E)
	fiducial_bearing_entry.grid(row = fid_row, column = 7, sticky = W)
	fiducial_edge_label.grid(row = fid_row, column = 8, sticky = E)
	fiducial_edge_entry.grid(row = fid_row, column = 9, sticky = W)

	deb1_row = fid_row + 1
	tag_pddb_label.grid(row = deb1_row, column = 0, sticky = E)
	tag_pddb_entry.grid(row = deb1_row, column = 1, sticky = W)
	tag_pddx_label.grid(row = deb1_row, column = 2, sticky = E)
	tag_pddx_entry.grid(row = deb1_row, column = 3, sticky = W)
	tag_pddy_label.grid(row = deb1_row, column = 4, sticky = E)
	tag_pddy_entry.grid(row = deb1_row, column = 5, sticky = W)
	clear_pnddbxy_button.grid(row = deb1_row, column = 6)

	deb2_row = deb1_row + 1
	tag_nddb_label.grid(row = deb2_row, column = 0, sticky = E)
	tag_nddb_entry.grid(row = deb2_row, column = 1, sticky = W)
	tag_nddx_label.grid(row = deb2_row, column = 2, sticky = E)
	tag_nddx_entry.grid(row = deb2_row, column = 3, sticky = W)
	tag_nddy_label.grid(row = deb2_row, column = 4, sticky = E)
	tag_nddy_entry.grid(row = deb2_row, column = 5, sticky = W)

	deb3_row = deb2_row + 1
	tag_addb_label.grid(row = deb3_row, column = 0, sticky = E)
	tag_addb_entry.grid(row = deb3_row, column = 1, sticky = W)
	tag_addx_label.grid(row = deb3_row, column = 2, sticky = E)
	tag_addx_entry.grid(row = deb3_row, column = 3, sticky = W)
	tag_addy_label.grid(row = deb3_row, column = 4, sticky = E)
	tag_addy_entry.grid(row = deb3_row, column = 5, sticky = W)

	# Bind mouse buttons to {map_canvas}:
	canvas.bind("<Button-1>", self.mouse_left)
	canvas.bind("<Button-2>", map_canvas.mouse_middle)
	canvas.bind("<Button-3>", map_canvas.mouse_right)

    def camera_on(self):
	""" {Application}: Deal with [Camera On] button. """

	self.map_canvas.camera_on()

    def camera_off(self):
	""" {Application}: Deal with [Camera Off] button. """

	self.map_canvas.camera_off()

    def camera_sync(self):
	""" {Application}: Deal with [Camera On] button. """

	self.map_canvas.camera_sync()

    def clear(self):
	""" {Application}: Deal with [Clear] check button. """

	# Clear out the tracking line for {camera} and {encoders}:
	map_canvas = self.map_canvas
	map_canvas.camera.lines_clear()
	map_canvas.encoders.lines_clear()

    def clear_pnddbxy(self):
	""" {Application}: Clear the postive/negative ddB/X/Y values. """

	# Grab latest camera values and use them as the anchor values:
	addb = self.camera_bearing
	addx = self.camera_x
	addy = self.camera_y
	# Load anchor values into {self}:
	self.addb = self.camera_bearing
	self.addx = self.camera_x
	self.addy = self.camera_y
	# Zero out the positive ddB/X/Y values:
	self.pddb = 0.0
	self.pddx = 0.0
	self.pddy = 0.0
	# Zero out the negative ddB/X/Y values:
	self.nddb = 0.0
	self.nddx = 0.0
	self.nddy = 0.0

    def goto(self):
	""" {Application}: Deal with [Go To] check button. """

	# Do nothing:
	print "[Go To] clicked", "goto_value=", self.goto_value.get()

    def grip(self):
	""" {Application}: Deal with [Grip] button. """

	# Do nothing:
	self.host_send("X", "1")
	print "[Grab] clicked"

    def halt(self):
	""" {Application}: Deal with [Halt] button. """

	self.host_send("H", "")

    def host_read(self, host_socket, mask):
	""" {Application}: Deal with data availablity from {host_socket}. """

	#FIXME: This code breaks if it does not end in a new line!!!
        #It should be totally rewritten:

	#print "file=", file, " mask=", mask
	data = host_socket.recv(4098)

	map_canvas = self.map_canvas
	pi = self.pi
	#print "host_read():data={0}\n".format(repr(data))
	lines = data.split('\n')
	for line in lines:
	    values = line.split(' ')
	    #print "ho2gui:values=", values
	    size = len(values)
	    #print "size=", size
	    if size != 0:
		#print "We have a command"
		command = values[0]
		if command == "camera" and size > 5:
                    # print "we have a camera position"

		    # Get the first camera {location}:
		    camera_tag_id = int(values[1])
		    camera_x = float(values[2])
		    camera_y = float(values[3])
		    camera_bearing = float(values[4]) * pi / 180.0
		    location = \
		      [camera_tag_id, camera_x, camera_y, camera_bearing]

		    # Load the first {location} into {locations}:
                    locations = []
		    locations.append(location)

                    # Now get the remaining {locations}:
		    camera_count = int(values[5])
		    for index in range(0, camera_count):
			offset = 6 + 4 * index
			tag_id = int(values[offset + 0])
			x = float(values[offset + 1])
			y = float(values[offset + 2])
			bearing = float(values[offset + 3]) * pi / 180.0
			locations.append( [tag_id, x, y, bearing] )

                    tag = self.map_canvas.tag_lookup(camera_tag_id)
		    tag_x = tag.x
		    tag_y = tag.y
		    tag_dx = camera_x - tag_x
                    tag_dy = camera_y - tag_y
		    tag_distance = math.sqrt(tag_dx * tag_dx + tag_dy * tag_dy)

		    addb = self.addb
		    addx = self.addx
		    addy = self.addy
                    ddb = camera_bearing - addb
                    ddx = camera_x - addx
                    ddy = camera_y - addy
		    
                    pddb = max(self.pddb, ddb)
                    pddx = max(self.pddx, ddx)
                    pddy = max(self.pddy, ddy)
                    nddb = min(self.nddb, ddb)
                    nddx = min(self.nddx, ddx)
                    nddy = min(self.nddy, ddy)

		    self.pddb = pddb
		    self.pddx = pddx
		    self.pddy = pddy
		    self.nddb = nddb
		    self.nddx = nddx
		    self.nddy = nddy

		    fiducial_x_entry = self.fiducial_x_entry
		    fiducial_x_entry.delete(0, END)
		    fiducial_x_entry.insert(0, values[2])
		    fiducial_y_entry = self.fiducial_y_entry
		    fiducial_y_entry.delete(0, END)
		    fiducial_y_entry.insert(0, values[3])
		    fiducial_bearing_entry = self.fiducial_bearing_entry
		    fiducial_bearing_entry.delete(0, END)
		    fiducial_bearing_entry.insert(0, values[4])
		    fiducial_tag_entry = self.fiducial_tag_entry
		    fiducial_tag_entry.delete(0, END)
		    fiducial_tag_entry.insert(0, values[5])
		    fiducial_edge_entry = self.fiducial_bearing_entry
		    fiducial_edge_entry.delete(0, END)
		    fiducial_edge_entry.insert(0, values[5])
		    tag_x_entry = self.tag_x_entry
		    tag_x_entry.delete(0, END)
		    tag_x_entry.insert(0, str(tag_x))
		    tag_y_entry = self.tag_y_entry
		    tag_y_entry.delete(0, END)
		    tag_y_entry.insert(0, str(tag_y))
		    tag_dx_entry = self.tag_dx_entry
		    tag_dx_entry.delete(0, END)
		    tag_dx_entry.insert(0, str(tag_dx))
		    tag_dy_entry = self.tag_dy_entry
		    tag_dy_entry.delete(0, END)
		    tag_dy_entry.insert(0, str(tag_dy))
		    tag_distance_entry = self.tag_distance_entry
		    tag_distance_entry.delete(0, END)
		    tag_distance_entry.insert(0, str(tag_distance))

		    tag_pddb_entry = self.tag_pddb_entry
		    tag_pddb_entry.delete(0, END)
		    tag_pddb_entry.insert(0, str(pddb))
		    tag_pddx_entry = self.tag_pddx_entry
		    tag_pddx_entry.delete(0, END)
		    tag_pddx_entry.insert(0, str(pddx))
		    tag_pddy_entry = self.tag_pddy_entry
		    tag_pddy_entry.delete(0, END)
		    tag_pddy_entry.insert(0, str(pddy))
		    tag_nddb_entry = self.tag_nddb_entry
		    tag_nddb_entry.delete(0, END)
		    tag_nddb_entry.insert(0, str(nddb))
		    tag_nddx_entry = self.tag_nddx_entry
		    tag_nddx_entry.delete(0, END)
		    tag_nddx_entry.insert(0, str(nddx))
		    tag_nddy_entry = self.tag_nddy_entry
		    tag_nddy_entry.delete(0, END)
		    tag_nddy_entry.insert(0, str(nddy))

		    tag_addb_entry = self.tag_addb_entry
		    tag_addb_entry.delete(0, END)
		    tag_addb_entry.insert(0, str(addb))
		    tag_addx_entry = self.tag_addx_entry
		    tag_addx_entry.delete(0, END)
		    tag_addx_entry.insert(0, str(addx))
		    tag_addy_entry = self.tag_addy_entry
		    tag_addy_entry.delete(0, END)
		    tag_addy_entry.insert(0, str(addy))

		    #print "GUI position:", " x=", x, " y=", y
		    #print "tag_id=", tag_id, "bearing=", bearing,
		    #print "tdist=", target_distance, "tbear=", target_bearing

		    # Redraw the camera polygon:
		    camera = map_canvas.camera
		    camera.update(locations)
		    camera.draw()

		elif command == "constants" and size > 18:
                    # print "we have some constants"

		    #print "line=", line
		    print "constants=", values, "size=", size

		    # Grab the constants from the command {values}:
		    bearing_limit = float(values[1])
		    speed_limit = int(values[2])
		    stall = int(values[3])
		    target_limit = float(values[4])
		    twist_limit = int(values[5])
		    ramp = int(values[6])
		    pid_p = float(values[7])
		    pid_i = float(values[8])
		    pid_d = float(values[9])
		    linear = float(values[10])
		    camera_dx = float(values[11])
		    camera_dy = float(values[12])
		    camera_twist = float(values[13])
		    grip_p = float(values[14])
		    grip_i = float(values[15])
		    grip_d = float(values[16])
		    left_force = int(values[17])
		    right_force = int(values[18])

		    # Grab the entry fields from {application}:
		    application = self.map_canvas.application
		    bearing_limit_entry = application.bearing_limit_entry
		    motor_stall_entry = application.motor_stall_entry
		    speed_limit_entry = application.speed_limit_entry
		    target_limit_entry = application.target_limit_entry
		    twist_limit_entry = application.twist_limit_entry
		    ramp_entry = application.ramp_entry
		    pid_p_entry = application.pid_p_entry
		    pid_i_entry = application.pid_i_entry
		    pid_d_entry = application.pid_d_entry
		    linear_entry = application.linear_entry
		    camera_dx_entry = application.camera_dx_entry
		    camera_dy_entry = application.camera_dy_entry
		    camera_twist_entry = application.camera_twist_entry
		    grip_p_entry = application.grip_p_entry
		    grip_i_entry = application.grip_i_entry
		    grip_d_entry = application.grip_d_entry
		    left_force_entry = application.left_force_entry
		    right_force_entry = application.right_force_entry

		    print "pid_p={0} pid_i={1} pid_d={2}". \
		      format(pid_p, pid_i, pid_d)
		    # Load the values into the entries:
		    bearing_limit_entry.delete(0, END)
		    bearing_limit_entry.insert(0, str(bearing_limit))
		    motor_stall_entry.delete(0, END)
		    motor_stall_entry.insert(0, str(stall))
		    speed_limit_entry.delete(0, END)
		    speed_limit_entry.insert(0, str(speed_limit))
		    target_limit_entry.delete(0, END)
		    target_limit_entry.insert(0, str(target_limit))
		    twist_limit_entry.delete(0, END)
		    twist_limit_entry.insert(0, str(twist_limit))
                    ramp_entry.delete(0, END)
                    ramp_entry.insert(0, str(ramp))
		    pid_p_entry.delete(0, END)
		    pid_p_entry.insert(0, str(pid_p))
		    pid_i_entry.delete(0, END)
		    pid_i_entry.insert(0, str(pid_i))
		    pid_d_entry.delete(0, END)
		    pid_d_entry.insert(0, str(pid_d))
		    linear_entry.delete(0, END)
		    linear_entry.insert(0, str(linear))
		    camera_dx_entry.delete(0, END)
		    camera_dx_entry.insert(0, str(camera_dx))
		    camera_dy_entry.delete(0, END)
		    camera_dy_entry.insert(0, str(camera_dy))
		    camera_twist_entry.delete(0, END)
		    camera_twist_entry.insert(0, str(camera_twist))
		    grip_p_entry.delete(0, END)
		    grip_p_entry.insert(0, str(grip_p))
		    grip_i_entry.delete(0, END)
		    grip_i_entry.insert(0, str(grip_i))
		    grip_d_entry.delete(0, END)
		    grip_d_entry.insert(0, str(grip_d))
		    left_force_entry.delete(0, END)
		    left_force_entry.insert(0, str(left_force))
		    right_force_entry.delete(0, END)
		    right_force_entry.insert(0, str(right_force))

		elif command == "encoders" and size > 5:
                    # print "we have an encoders position"

		    x = float(values[1])
		    y = float(values[2])
		    bearing = float(values[3]) * pi / 180.0
		    target_bearing = float(values[4]) * pi / 180.0
		    target_distance = float(values[5])

		    reckon_x_entry = self.reckon_x_entry
		    reckon_x_entry.delete(0, END)
		    reckon_x_entry.insert(0, values[1])
		    reckon_y_entry = self.reckon_y_entry
		    reckon_y_entry.delete(0, END)
		    reckon_y_entry.insert(0, values[2])
		    reckon_bearing_entry = self.reckon_bearing_entry
		    reckon_bearing_entry.delete(0, END)
		    reckon_bearing_entry.insert(0, values[3])
		    target_bearing_entry = self.target_bearing_entry
		    target_bearing_entry.delete(0, END)
		    target_bearing_entry.insert(0, values[4])
		    target_distance_entry = self.target_distance_entry
		    target_distance_entry.delete(0, END)
		    target_distance_entry.insert(0, values[5])

		    # Redraw the robot polygon outline:
		    map_canvas = self.map_canvas
		    encoders = map_canvas.encoders
		    encoders.update(x, y, bearing, \
		      target_distance, target_bearing)
		    encoders.draw()

		elif command == "segment" and size > 4:
		    #print "we have a segment"

		    # Extract tag {values}:
		    tag1_id = int(values[1])
		    way1_id = int(values[2])
		    tag2_id = int(values[3])
		    way2_id = int(values[4])

		    # Lookup {tag1} and {tag2}:
		    tag1 = map_canvas.tag_lookup(tag1_id)
		    tag2 = map_canvas.tag_lookup(tag2_id)

		    # Lookup {way1} and {way2}:
		    way1 = tag1.way_lookup(way1_id)
		    way2 = tag2.way_lookup(way2_id)

		    # Now create the {segment}:
		    segment = way1.pair(way2, False)
		    segment.draw()

		elif command == "tag" and size > 5:
                    print "tag ", values
		    #print "we have a tag"

		    # Extract tag {values}:
		    tag_id = int(values[1])
		    tag_x = float(values[2])
		    tag_y = float(values[3])
		    tag_angle = float(values[4]) * pi / 180.0
		    tag_edge_length = float(values[5])

		    # Lookup {tag}:
		    tag = map_canvas.tag_lookup(tag_id)

		    # Update {tag} and draw it:
		    tag.update(tag_x, tag_y, tag_angle, tag_edge_length)
		    tag.draw()

		elif command == "way" and size > 6:
		    print "way values=", values

		    # Extract way point {values}:
		    way_tag_id = int(values[1])
		    way_id = int(values[2])
		    way_dx = float(values[3])
		    way_dy = float(values[4])
		    way_angle = float(values[5]) * pi / 180.0
		    way_name = values[6].strip('"')
		    way_height = float(values[7])
		    way_open_width = float(values[8])
		    way_close_width = float(values[9])
		    way_flags = values[10].strip('"')

		    # Lookup {tag} and {way} point:
		    assert way_tag_id != 0
                    tag = map_canvas.tag_lookup(way_tag_id)
		    way = tag.way_lookup(way_id)

		    # Update {way} contents and draw it:
		    way.update(way_dx, way_dy, way_angle, way_name, \
		      way_height, way_open_width, way_close_width, way_flags, \
		      host_notify = False)
		    way.draw()

		elif command == "neighbor":
		    # We do not show the neighbor relation, so we just drop it:
		    command = command

		#else:
		#    print "ignoring '{0}'".format(command)

    def host_send(self, command, arguments):
	""" {Application}: Send {command} with {arguments} to host socket. """

	if arguments == "":
	    self.host_socket.send("{0}\n".format(command))
	    print "G2H:{0}".format(command)
	else:
	    self.host_socket.send("{0} {1}\n".format(command, arguments))
	    print "G2H:{0} {1}".format(command, arguments)

    def move(self):
	""" {Application}: Deal with [Move] button. """

	self.map_canvas.move()

    def mouse_left(self, event):
	""" {Application}: Deal with left mouse click. """

	self.map_canvas.mouse_left(event)

	self.way_create_button.configure(state = NORMAL)

    def release(self):
	""" {Application}: Deal with [Release] button. """

	print "[Release] clicked"
	self.host_send("X", "0")

    def save(self):
	""" {Application}: Deal with [Save] button click. """

	self.host_send("V", "")

    def show(self):
	""" {Application}: Deal with [Show] button click.  """

	self.map_canvas.show()
	print ""

    def constants_update(self):
	""" {Application}: Deal with [Const Update] constants button click. """

	# Extract all the values from the entry fields:
        bearing_limit = float(self.bearing_limit_entry.get())
        stall = int(self.motor_stall_entry.get())
        speed_limit = int(self.speed_limit_entry.get())
        twist_limit = int(self.twist_limit_entry.get())
        target_limit = float(self.target_limit_entry.get())
	ramp = int(self.ramp_entry.get())
	pid_p = float(self.pid_p_entry.get())
	pid_i = float(self.pid_i_entry.get())
	pid_d = float(self.pid_d_entry.get())
	linear = float(self.linear_entry.get())
	camera_dx = float(self.camera_dx_entry.get())
	camera_dy = float(self.camera_dy_entry.get())
	camera_twist = float(self.camera_twist_entry.get())
	grip_p = float(self.grip_p_entry.get())
	grip_i = float(self.grip_i_entry.get())
	grip_d = float(self.grip_d_entry.get())
	left_force = int(self.left_force_entry.get())
	right_force = int(self.right_force_entry.get())

	# Send the "C" command off to the host:
	arguments1 = "{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}"
	arguments2 = " {10} {11} {12} {13} {14} {15} {16} {17}"
	arguments = (arguments1 + arguments2). \
	  format(bearing_limit, speed_limit, stall, target_limit, twist_limit, \
	  ramp, pid_p, pid_i, pid_d, linear, camera_dx, camera_dy, \
	  camera_twist, grip_p, grip_i, grip_d, left_force, right_force)
	self.host_send("C", arguments)

    def unmove(self):
	""" {Application}: Deal with [Move] button. """

	self.map_canvas.unmove()

    def way_create(self):
	""" {Application}: Deal with [Way Delete] button click.  """

	self.map_canvas.way_create()

    def way_delete(self):
	""" {Application}: Deal with [Way Delete] button click.  """

	self.map_canvas.way_delete()

    def way_goto(self):
	""" {Application}: Deal with [Way Go To] button. """

	#print "[Way Go To] clicked"

	self.map_canvas.way_goto()

    def way_grab(self):
	""" {Application}: Deal with [Way Grab] button. """

	self.map_canvas.way_grab()

    def way_release(self):
	""" {Application}: Deal with [Way Release] button. """

	self.map_canvas.way_release()

    def way_update(self):
	""" {Application}: Deal with [Way_Update] button click. """

	# Extract all the values from the entry fields:

	print "Application.way_update()"

	# Grab the selected way:
	map_canvas = self.map_canvas
	way = map_canvas.selected_way
	if way != None:
	    # Grab the values from the GUI:
            way.gui_read()

	    # Ship them on the way:
            way.send()

class Camera:
    def __init__(self, map_canvas):
	""" {Camera}: Create {self} object containing {map_canvas}. """

	# Load up {self}
	self.colors = ("red", "magenta", "cyan", "green", "sky blue", \
	  "orange", "blue", "hot pink", "black")
	self.last_x = 0.0
	self.last_y = 0.0
	self.lines = []
	self.locations = []
	self.map_canvas = map_canvas
	self.polygons = []
	self.robot_outline = ((-2, -2), (2, -2), (4, 0), (2, 2), (-2, 2))
	self.tag_lines = []

    def draw(self):
	""" {Camera}: Draw {self}. """

	# Grab some values from {Camera}:
	polygons = self.polygons
	tag_lines = self.tag_lines
	locations = self.locations
	map_canvas = self.map_canvas

	# Clear out {polygons}:
	for polygon in self.polygons:
	    map_canvas.delete(polygon)
	del polygons[:]

	# Clear out {lines}:
	for tag_line in self.tag_lines:
	    map_canvas.delete(tag_line)
	del tag_lines[:]

	# Draw the polygon for {self}:
	fill = True
	for location in self.locations:
	    self.robot_draw(location, fill)
	    fill = False

    def lines_clear(self):
	""" {Camera}: Clear all lines drawn. """

	# Extract some values from {self}:
	lines = self.lines
	map_canvas = self.map_canvas

	# Clear all of the lines:
	for line in lines:
	    map_canvas.delete(line)

	# Clear out {lines}:
	del lines[:]

	# Remember that we cleared all of the lines:
	self.tag_id = -1

    def robot_draw(self, location, fill):
	""" {Camera}: Draw a robot outline for {location}.  If {fill} is
	    {True}, the robot is filled in. """

	# Grab some values from {self}:
	colors = self.colors
	map_canvas = self.map_canvas
	polygons = self.polygons
	tag_lines = self.tag_lines
	robot_outline = self.robot_outline

	# Extract values from location:
	tag_id = location[0]
	x = location[1]
	y = location[2]
	bearing = location[3]

	# Compute the color to use:
	#print "colors=", colors
	color = colors[tag_id % len(colors)]
	#print "tag_id={0} color={1}".format(tag_id, color)

	# Draw the polygon for {self}:
	fill_color = ""
	if fill:
	    fill_color = color
	polygon = map_canvas.polygon(x, y, bearing, fill_color, color, \
	  robot_outline)
	polygons.append(polygon)

	# Draw line to tag:
	tag = map_canvas.tag_lookup(tag_id)
	tag_line = map_canvas.line(x, y, tag.x, tag.y, color)
	tag_lines.append(tag_line)

    def update(self, locations):
	""" {Camera}: Update the {self} to contain {locactions}. """

	# Add a connecting line:
	if len(locations) > 0:
	    # Draw the {path_line}:
	    location = locations[0]
	    tag_id = location[0]
	    x = location[1]
            y = location[2]
	    bearing = location[3]

            # Draw next segment of path:
	    map_canvas = self.map_canvas
	    path_line = map_canvas.line(self.last_x, self.last_y, x, y, "blue")
	    self.last_x = x
	    self.last_y = y

	    # Compute end points of a bar that is perpendicual to the bearing:
	    pi = map_canvas.application.pi

	    # Compute perpendicular {angle}:
	    angle = bearing + pi / 2.0
            if angle > pi:
		angle = angle - pi - pi
	    elif angle < -pi:
		angle = angle + pi + pi

	    half_bar = 1.0		# Half the bar length
	    cosine_angle = math.cos(angle)
	    sine_angle = math.sin(angle)
	    half_bar_cosine_angle = half_bar * cosine_angle
	    half_bar_sine_angle = half_bar * sine_angle

	    # Bar {color} depends upon low order bits of {tag_id}:
	    colors = ("CadetBlue", "DarkBlue", "DarkViolet", "DarkCyan") 
	    color = colors[tag_id & 3]

	    # Draw the {bearing_line}:
	    x1 = x - half_bar_cosine_angle
	    y1 = y - half_bar_sine_angle
	    x2 = x + half_bar_cosine_angle
	    y2 = y + half_bar_sine_angle
	    #bearing_line = map_canvas.line(x1, y1, x2, y2, color)

            # Keep track of the {lines}:
	    lines = self.lines
	    self.lines.append(path_line)
	    #self.lines.append(bearing_line)
	
	# Load up {self}:
	self.locations = locations

class Encoders:
    def __init__(self, map_canvas):
	""" {Encoders}: Create {self} object containing {map_canvas}. """

	# Load up {self}:
	self.map_canvas = map_canvas
	self.polygon = -1
	self.line = -1
	self.lines = []
	self.target_distance = -1
	self.update(0.0, 0.0, 0.0, -1.0, 0.0)

    def draw(self):
	""" {Encoders}: Draw the {self}. """

	# Draw the encoder robot polygon:
	map_canvas = self.map_canvas
	map_canvas.delete(self.polygon)
	x = self.x
	y = self.y
	bearing = self.bearing
	self.polygon = \
	  map_canvas.polygon(x, y, bearing, "", "blue", \
	  ((-4, -4), (4, -4), (8, 0), (4, 4), (-4, 4)))

	# Draw the target line:
	#print "x=", x, "y=", y
	#print "tdist=", self.target_distance, "tbear=", self.target_bearing
	map_canvas.delete(self.line)
	pi = map_canvas.application.pi
	target_distance = self.target_distance
	target_bearing = self.target_bearing
	#print "angle=", angle * 180.0 / pi
	self.line = map_canvas.line(x, y, \
	  x + target_distance * math.cos(target_bearing), \
	  y + target_distance * math.sin(target_bearing), "blue")

    def lines_clear(self):
	""" {Encoders}: Clear all of the lines in {self}. """

	# Extract some values from {self}:
	lines = self.lines
	map_canvas = self.map_canvas

	# Clear all of the lines:
	for line in lines:
	    map_canvas.delete(line)

	# Clear out {lines}:
	del lines[:]

	# Remember that we cleared all of the lines:
	self.target_distance = -1

    def update(self, x, y, bearing, target_distance, target_bearing):
	""" {Encoders}: Update {self} to contain {x}, {y}, {bearing},
	    {target_distance}, and {target_bearing}. """


	# Draw any line tracking:
	if self.target_distance >= 0.0:
	    # Draw {path_line}:
	    old_x = self.x
	    old_y = self.y
	    map_canvas = self.map_canvas
	    path_line = map_canvas.line(old_x, old_y, x, y, "green")

	    # Compute end points of a bar that is perpendicual to the bearing:
	    pi = map_canvas.application.pi
	    angle = bearing + pi / 2.0	# Perprendicular angle
            if angle > pi:
		angle = angle - pi - pi
	    elif angle < -pi:
		angle = angle + pi + pi
	    half_bar = 2.0		# Half the bar length
	    cosine_angle = math.cos(angle)
	    sine_angle = math.sin(angle)
	    half_bar_cosine_angle = half_bar * cosine_angle
	    half_bar_sine_angle = half_bar * sine_angle

	    # Draw the {bearing_line}:
	    x1 = x - half_bar_cosine_angle
	    y1 = y - half_bar_sine_angle
	    x2 = x + half_bar_cosine_angle
	    y2 = y + half_bar_sine_angle
	    #bearing_line = map_canvas.line(x1, y1, x2, y2, "maroon")

	    # Keep track of {path_line} and {bearing_line}:
	    lines = self.lines
	    lines.append(path_line)
	    #lines.append(bearing_line)

	# Load up {self}:
	self.x = x
	self.y = y
	self.bearing = bearing
	self.target_distance = target_distance
	self.target_bearing = target_bearing

class Map_Canvas:
    """ A {Map_Canvas} deals with the different coordinate spaces between
	a {Tkinter} canvas and a regular Cartesian coordinate space.  A
	{Map_Canvas} can perform offseting and scaling as well. """

    def __init__(self, canvas, width, height, application):
	""" {Map_Canvas}: Create new {Map_Canvas} containing {canvas}, {width},
	    {height}, and {application}. """

	self.application = application
	self.canvas = canvas
	self.camera = Camera(self)
	self.encoders = Encoders(self)
	self.grab_way = None
	self.height = height
	self.release_way = None
	self.scale = 4
	self.segments = {}
	self.selected_tag = None
	self.selected_way = None
	self.tags = {}
	self.target = Target(self)
	self.ways = []
	self.width = width
	# Oligic values:
	#self.x_offset = 60
	#self.y_offset = 40
	# Home values:
	self.x_offset = 10
	self.y_offset = 10
	
    def camera_off(self):
	""" {Map_Canvas}: Turn robot camera off. """

	self.application.host_send("E", "0")

    def camera_on(self):
	""" {Map_Canvas}: Turn robot camera on. """

	self.application.host_send("E", "1")

    def camera_sync(self):
	""" {Map_Canvas}: Turn robot camera on. """

	self.application.host_send("Y", "0")

    def delete(self, item):
	""" {Map_Canvas}: delete item from {self}. """

	# Only delete {item} if it exists (i.e. > 0):
	if item >= 0:
	    # Delete {item} from canvas:
	    self.canvas.delete(item)

    def line(self, x1, y1, x2, y2, line_color):
	""" {Map_Canvas}: draw {line_color} line from ({x1},{y1}) to
	    ({x2},{y2}). """

	#print "x1=", x1, " y1=", y1, " x2=", x2, " y2=", y2

	return self.canvas.create_line( \
	  (self.x(x1), self.y(y1), self.x(x2), self.y(y2)), \
	  fill = line_color)

    def mouse_left(self, event):
	""" {Map_Canvas}: Deal with a left button mouse event. """

	# Extract {event_x} and {event_y} from {event}:
	event_x = float(event.x)
	event_y = float(event.y)

	# Convert from canvas coordinates to cartisian coordinates:
	scale = self.scale
	map_x = event_x / scale - self.x_offset
	map_y= (self.height - event_y) / scale - self.y_offset

	# Update {target}:
	target = self.target
	target.update(map_x, map_y)
	target.draw()

	# Find closest tag (if any):
	tags = self.tags
	closest_tag = None
	closest_distance = 123456789.0
	for tag_id in tags:
	    tag = self.tag_lookup(tag_id)
	    if tag != None:
		dx = tag.x - map_x
		dy = tag.y - map_y
		distance = math.sqrt(dx * dx + dy * dy)
		if distance < closest_distance:
		    closest_distance = distance
		    closest_tag = tag

	# If we have a closest tag, delselect any previous tag and
	# select this one:
	if closest_tag != None:
	    selected_tag = self.selected_tag
	    if selected_tag == closest_tag:
		# The user has clicked the same tag again, deselect it:
		selected_tag.deselect()
	    else:
                # The user has clicked on a new tag (or a first tag):
		if selected_tag != None:
		    # Deselect any preiously selected tag:
		    selected_tag.deselect()

		# Select {closest_tag}:
		closest_tag.select()

	# Ship the new target location off to the Host when in "goto" mode:
	application = self.application
	if application.goto_value.get():
            arguments = "{0} {1}".format(map_x, map_y)
	    self.application.host_send("Z", arguments)

    def mouse_middle(self, event):
	""" {Map_Canvas}: Deal with a middle mouse click. """

	# Ship the new target location off to the Host:
	x = float(event.x)
	y = float(event.y)

	print "map_canvas.mouse_middle:", "x=", x, "y=", y, "num=", event.num

	scale = self.scale
	map_x = x / scale - self.x_offset
	map_y = (self.height - y) / scale - self.y_offset


    def mouse_right(self, event):
	""" {Map_Canvas}: Deal with a right mouse click {event}. """

	# Ship the new target location off to the Host:
	event_x = float(event.x)
	event_y = float(event.y)

	#print "Map_Canvas.mouse_right", \
	#  "event_x=", event_x, "event_y=", event_y, "num=", event.num

	# Convert from {canvas} coordinate space to cartisian coordinate space:
	scale = self.scale
	x = event_x / scale - self.x_offset
	y = (self.height - event_y) / scale - self.y_offset

	# Search for closest {Way} to mouse click:
	closest_distance = 99999999.9
	closest_way = None
	ways = self.ways
	for way in self.ways:
            # Compute distance between mouse click and {Way}:
            tag = way.tag
            dx = tag.x + way.dx - x
            dy = tag.y + way.dy - y
	    distance =  math.sqrt(dx * dx + dy * dy)

            # Is mouse click close enough to a {Way}:
            if distance < closest_distance and distance < 10.0:
		# Yes, it is:
		closest_distance = distance
		closest_way = way

	# Only process {closest_way} if it was close enough to mouse click:
	if closest_way != None:
	    # We do different things depending upon {selected_way}:
	    selected_way = self.selected_way
	    if selected_way == None:
		# There is no {selected_way}; select {closest_way}:
		self.way_select(closest_way)
		print "first selection"
	    else:
		# We have a {selected_way}:
		if closest_way == selected_way:
		    # We clicked on {selected_way}, so clear selection:
		    self.way_deselect()
		    print "deselect"
       		else:
		    # Deal with {Segment} between the two:
		    segment = self.segment_lookup(closest_way, selected_way)

		    # Figure out whether the segment is drawn:
		    closest_segments = closest_way.segments
		    selected_segments = selected_way.segments
		    in_closest = segment in closest_segments
		    in_selected = segment in selected_segments

                    closest_tag = closest_way.tag
                    map_canvas = closest_tag.map_canvas
		    application = map_canvas.application

		    if in_closest and in_selected:
			# {segment} drawn; remove connection:
			segment.clear()
			segment.delete()
			print "segment disconnect"
		    elif not in_closest and not in_selected:
			# {segment} not connected; perform connection:
			segment = closest_way.pair(selected_way, True)
			print "segment connect"
		    else:
			print "Inconsistent tag.segments data structures"

                    # Do final selection:
		    self.way_select(closest_way)

    def move(self):
	""" {Map_Canvas}: Deal with [Move] button. """

	grab_way = self.grab_way
	release_way = self.release_way
	if grab_way != None and release_way != None:
	    arguments = '"{0}" "{1}"'.format(grab_way.name, release_way.name)
	    self.application.host_send("M", arguments)
	else:
	    print "No grab and/or release way"

    def polygon(self, x, y, angle, fill_color, outline_color, pairs):
	""" {Map_Canvas}: Draw a polygon consisting of {pairs} at ({x},{y})
	    rotated by {angle} with an outline of {outline_color} and an
	    interior color of {fill_color}. """

	#print "x=", x, " y=", y, " angle=", angle, " pairs=", pairs

	coordinates = []
	for pair in pairs:
	    dx = float(pair[0])
	    dy = float(pair[1])
            length = math.sqrt(dx * dx + dy * dy)
	    rotate = angle + math.atan2(dy, dx)
	    #print "dx=", dx, " dy=", dy, " length=", length
            coordinates.append(self.x(x + length * math.cos(rotate)))
            coordinates.append(self.y(y + length * math.sin(rotate)))

	#print "coordinates=", coordinates

	return self.canvas.create_polygon(coordinates, \
	  fill = fill_color, outline = outline_color)

    def rectangle(self, x, y, dx, dy, fill_color):
	""" {Map_Canvas}: Draw a rectangle that is {dx} wide, {dy} high,
	    and centered at ({x}, {y}). """

	#print "x=", x, " y=", y, " dx=", dx, " dy=", dy

        half_dx = dx / 2.0
	half_dy = dy / 2.0
	return self.canvas.create_rectangle( \
	  (self.x(x - half_dx), self.y(y - half_dy), \
	   self.x(x + half_dx), self.y(y + half_dy)), \
	  fill = fill_color)

    def segment_lookup(self, way1, way2, label = "none"):
	""" {Map_Canvas}: Return {Segment} that contains {way1} and {way2}. """

	#print "segment_lookup:", \
	#  "t1=", way1.tag.id, "w1=", way1.id, \
	#  "t2=", way2.tag.id, "w2=", way2.id, \
	#  "label=", label

	# Extract some valuse from {way1} and {way2}:
	way1_tag = way1.tag
	way2_tag = way2.tag
	way1_tag_id = way1_tag.id
	way2_tag_id = way2_tag.id
	way1_id = way1.id
	way2_id = way2.id

	# Compute the segment key:
	if way1_tag.id < way2_tag.id or \
	  way1_tag_id == way2_tag_id and way1_id < way2_id:
	    segment_key = (way1_tag_id, way1_id, way2_tag_id, way2_id)
	else:
	    segment_key = (way2_tag_id, way2_id, way1_tag_id, way1_id)
	#print "segment_key=", segment_key
	
	# Make sure we have a unique {segment} in {segments}:
	segments = self.segments
	if segment_key in segments:
	    # We already have the segment:
	    segment = segments[segment_key]
            #print "segment exists"
	else:
	    # We need to create segment:
	    segment = Segment(way1, way2)
            segments[segment_key] = segment
	    #print "segment_create"

	#print "segment_lookup:", \
	#  "st1=", segment.way1.tag.id, "sw1=", segment.way1.id, \
	#  "st2=", segment.way2.tag.id, "sw2=", segment.way2.id

	return segment

    def show(self, label = ""):
	""" {Map_Canvas}: Show contents of {self} prefixed by {label}. """

	for tag in self.tags.values():
	    tag.show(label)

    def tag_lookup(self, tag_id):
	""" {Map_Canvas}: Return the Tag associated with {tag_id}. """

	tags = self.tags
	if tag_id in tags:
	    tag = tags[tag_id]
	else:
	    tag = Tag(tag_id, self)
	    tags[tag_id] = tag
	return tag

    def unmove(self):
	""" {Map_Canvas}: Deal with [UnMove] button. """

	grab_way = self.grab_way
	release_way = self.release_way
	if grab_way != None and release_way != None:
	    arguments = '"{0}" "{1}"'.format(release_way.name, grab_way.name)
	    self.application.host_send("M", arguments)
	else:
	    print "No grab and/or release way"

    def way_create(self):
	""" {Map_Canvas}: Deal with click of [Way Create] button click. """

	#print "[Way Create] button pressed"

	target = self.target
	x = target.x
	y = target.y

	# Find the closest {Tag}:
	tags = self.tags
	closest_distance = 99999999.9
	closest_tag = None
	for tag in tags.values():
	    dx = tag.x - x
            dy = tag.y - y
            distance = math.sqrt(dx * dx + dy * dy)
	    if distance < closest_distance:
		closest_distance = distance
		closest_tag = tag

	# Only create a way if we can find {closest_tag}:
	if closest_tag != None:
	    # Now compute the {greatest_id} in {ways}:
	    greatest_id = -1
            ways = closest_tag.ways
	    for way in ways.values():
		way_id = way.id
		if way_id > greatest_id:
		    greatest_id = way_id

            # Get the {Way} associated with {new_id}:
	    new_id = greatest_id + 1            
	    new_way = closest_tag.way_lookup(new_id)
	    new_way.update(x - closest_tag.x, y - closest_tag.y, \
	      0.0, "", 0.0, 0.0, 0.0, "")

            # Now we can draw it:
	    new_way.draw()

    def way_delete(self):
	""" {Map_Canvas}: delete most recently selected {Way} from {self}. """

	# Is there a {selected_way}:
	selected_way = self.selected_way
	if selected_way != None:
	    # Delete {way}:
	    self.way_deselect()
	    selected_way.delete()
	    self.ways.remove(selected_way)

    def way_deselect(self):
	""" {Map_Canvas}: deselect currently selected {Way}. """

	selected_way = self.selected_way
	if selected_way != None:
	    # Get {selected_way} color changed and redrawn:
	    selected_way.deselect()
	    selected_way.draw()

	    # Mark that there is no {selected_way}:
            self.selected_way = None

	    # Disable some way buttons, since there is no {Way} selected:
	    application = self.application
	    application.way_delete_button.configure(state = DISABLED)
	    application.way_goto_button.configure(state = DISABLED)
	    application.way_grab_button.configure(state = DISABLED)
	    application.way_release_button.configure(state = DISABLED)

	    # Send any 
	    if selected_way.gui_read():
		selected_way.send()

	    # Clear out any fields:
	    selected_way.gui_clear()

    def way_goto(self):
	""" {Map_Canvas}: Goto selected {Way}. """

	selected_way = self.selected_way
	if selected_way != None:
	    arguments = '"{0}"'.format(selected_way.name)
	    self.application.host_send("G",  arguments)

    def way_grab(self):
	""" {Map_Canvas}: Deal with [Way Grab] button. """

	# Make sure {selected_way} is points to a real {Way}:
	selected_way = self.selected_way
	if selected_way != None:
	    # Overwrite any previous version of {grab_way}:
	    previous_grab_way = self.grab_way
	    grab_way = selected_way
	    self.grab_way = grab_way

	    # Ensure {release_way} and {grab_way} do not reference same {Way}:
	    release_way = self.release_way
	    if release_way == grab_way:
		# They match, so clear {release_way}:
		self.release_way = None
		release_way.draw()
		release_way = None

	    # Redraw the {previous_grab_way} and the current {grab_way}:
	    if previous_grab_way != None:
		previous_grab_way.draw()
	    grab_way.draw()

            # Now enable/disable [Move] button:
            move_button = self.application.move_button
	    unmove_button = self.application.unmove_button
	    if grab_way != None and release_way != None:
		move_button.configure(state = NORMAL)
		unmove_button.configure(state = NORMAL)
	    else:
		move_button.configure(state = DISABLED)
		unmove_button.configure(state = DISABLED)

    def way_release(self):
	""" {Map_Canvas}: Deal with [Way Release] button. """

	# Make sure {selected_way} is points to a real {Way}:
	selected_way = self.selected_way
	if selected_way != None:
	    # Overwrite any previous version of {grab_way}:
	    previous_release_way = self.release_way
	    release_way = selected_way
	    self.release_way = release_way

	    # Ensure {grab_way} and {release_way} do not reference same {Way}:
	    grab_way = self.grab_way
	    if grab_way == release_way:
		# They match, so clear {grap_way}:
		self.grab_way = None
		grab_way.draw()
		grab_way = None

	    # Redraw the {previous_release_way} and the current {release_way}:
	    if previous_release_way != None:
		previous_release_way.draw()
	    release_way.draw()

            # Now enable/disable [Move] button:
            move_button = self.application.move_button
	    unmove_button = self.application.unmove_button
	    if grab_way != None and release_way != None:
		move_button.configure(state = NORMAL)
		unmove_button.configure(state = NORMAL)
	    else:
		move_button.configure(state = DISABLED)
		unmove_button.configure(state = DISABLED)

    def way_select(self, way):
	""" {Map_Canvas}: Select {way} as the currently selected {Way}. """

	self.way_deselect()
	self.selected_way = way
	way.select()
	way.draw()
	application = self.application
	application.way_delete_button.configure(state = NORMAL)
	application.way_goto_button.configure(state = NORMAL)
	
	height = way.height
	open_width = way.open_width
	flags = way.flags
	if height != None and open_width != None and flags != None and \
	  height > 2.0 and open_width > 0.5 and 'b' in flags:
	    application.way_grab_button.configure(state = NORMAL)
	    application.way_release_button.configure(state = NORMAL)
	else:
	    application.way_grab_button.configure(state = DISABLED)
	    application.way_release_button.configure(state = DISABLED)

	#application.way_move_button.configure(state = NORMAL)
	way_name_entry = application.way_name_entry
	way_name_entry.delete(0, END)
	way_name_entry.insert(0, way.name)


    def x(self, x):
	""" {Map_Canvas}: Return the X coordinate corresponding to {x}.  """

	result = (x + self.x_offset) * self.scale
	#print "x(", x, ")=", result
	return result

    def y(self, y):
	""" {Map_Canvas}: Return the Y coordinate corresponding to {y}.  """

	result = self.height - (y + self.y_offset) * self.scale
	#print "y(", y, ")=", result
	return result


class Segment:
    """ A {Segment} represents the ability for the robot to go straight
	between two way points. """

    def __init__(self, way1, way2):
	""" {Segment}: create segment path that bridges {way1} and {way2}. """

	# Extract {Tag}'s and id's from {way1} and {way2}:
	id1 = way1.id
	id2 = way2.id
	tag1 = way1.tag
	tag2 = way2.tag

	# Check for identical tag values:
	if tag1 == tag2 and id1 == id2:
	    print "Creating segment with idential tags"

	# Keep {way1} and {way2} in asscending order by {Tag} id:
	if id1 > id2:
            # Swap {way1} and {way2}:
	    way1, way2 = way2, way1

	# Load up {self}.  Start as {self.deleted} as {True},
	# {Map_Canvas.segment_lookup}() will set to {False}:
	self.deleted = True
	self.line = -1
	self.way1 = way1
	self.way2 = way2

    def clear(self):
	""" {Segment}: remove {self} from associated canvas. """

	self.way1.tag.map_canvas.delete(self.line)

    def delete(self):
	""" {Segment}: delete {self}. """

	# Erase the line from the display:
	self.clear()

	# Extract some values from {self}:
	way1 = self.way1
	way2 = self.way2
	way1_tag = way1.tag
	way2_tag = way2.tag
	way1_segments = way1.segments
	way2_segments = way2.segments
	map_canvas = way1_tag.map_canvas

	# Extract the segments:

	# Remove {self} from the segments list of each way point:
	if self in way1_segments:
	    way1_segments.remove(self)
	if self in way2_segments:
	    way2_segments.remove(self)

	# Let the host know that the segment is gone:
	arguments = "{0} {1} {2} {3}". \
	  format(way1_tag.id, way1.id, way2_tag.id, way2.id)
	map_canvas.application.host_send("R", arguments)
	
	# Make sure that {self} is not already deleted:
	if self.deleted:
	    print "Deleting segment that is marked as deleted already."

	# Make as deleted now, so that the next time
	# {Map_Canvas.segment_lookup}() is called it can notice
	# that it is re-creating it:
	self.deleted = True

    def draw(self):
	""" {Segment}: draw {self} on associated canvas. """

	way1 = self.way1
	way2 = self.way2
	tag1 = way1.tag
	tag2 = way2.tag

	map_canvas = tag1.map_canvas
	self.clear()
	self.line = map_canvas.line( \
	  tag1.x + way1.dx, tag1.y + way1.dy, \
	  tag2.x + way2.dx, tag2.y + way2.dy, "orange")


    def show(self, label = ""):
	""" {Segment}: show the contents of {self}. """

	print "    %s Segment %d %d -- %d %d" % (label, \
	  self.way1.tag.id, self.way1.id, self.way2.tag.id, self.way2.id)


class Tag:
    """ A {Tag} represents a ceiling fiducial. """

    def __init__(self, id, map_canvas):
	""" {Tag}: return a new {Tag} that contains {id} and {map_canvas}. """

	assert id != 0

	# Load up {self}:
	self.angle = 0.0
	self.color = "light gray"
	self.edge_length = 0.0
	self.id = id
	self.map_canvas = map_canvas
	self.polygon = -1
	self.ways = {}
	self.x = 0.0
	self.y = 0.0

	# Kludge to force a way point on top of {self}:
	#way = self.way_lookup(0)
	#way.update(0.0, 0.0, 0.0)

    def deselect(self):
	""" {Tag}: Cause {self} to be deselected. """

        # Grab some values from {application}:
	application = self.map_canvas.application
	fiducial_tag_entry = application.fiducial_tag_entry
	fiducial_x_entry = application.fiducial_x_entry
	fiducial_y_entry = application.fiducial_y_entry
	fiducial_bearing_entry = application.fiducial_bearing_entry
	fiducial_edge_entry = application.fiducial_edge_entry

	# Read current value from {fiducial_edge_entry}:
        edge_length = float(fiducial_edge_entry.get())

	# Did it change?:
	if edge_length != self.edge_length:
	    # Yes, it changed.  Record the change back into {self}:
            self.edge_length = edge_length

	    #print "old_edge_length={0} new_edge_length={1}". \
	    #  format(self.edge_length, edge_length)

	    # The send the updated information back to the host:
	    application.host_send("T", "{0} {1} {2} {3} {4:.4f}". \
	      format(self.id, self.x, self.y, \
	      self.angle * 180.0 / application.pi, edge_length))

	# Now forget that {self} is selected:
	self.map_canvas.selected_tag = None

	# Clear out the GUI entries:
	fiducial_tag_entry.delete(0, END)
	fiducial_x_entry.delete(0, END)
	fiducial_y_entry.delete(0, END)
	fiducial_bearing_entry.delete(0, END)
	fiducial_edge_entry.delete(0, END)

	# Redraw {self} in the default color:
	self.color = "light gray"
	self.draw()

    def draw(self):
	""" {Tag}: Draw {self} on associated canvas. """

	polygon = self.polygon
	map_canvas = self.map_canvas
	map_canvas.delete(polygon)

	edge_length = self.edge_length
	half_edge = edge_length / 2.0
	pairs = ( \
	  (-half_edge, -half_edge) , \
	  ( half_edge, -half_edge) , \
	  ( half_edge,  half_edge) , \
	  (-half_edge,  half_edge) )
	#print "pairs=", pairs

	self.polygon = map_canvas.polygon(self.x, self.y,
	  self.angle, self.color, "black", pairs)

	#self.rect = map_canvas.rectangle(self.x, self.y, 4, 4, self.color)

	for way in self.ways.values():
	    way.draw()

    def select(self):
	""" {Tag}: Cause {self} to be selected. """

        # Grab some values from {application}:
	application = self.map_canvas.application
	fiducial_tag_entry = application.fiducial_tag_entry
	fiducial_x_entry = application.fiducial_x_entry
	fiducial_y_entry = application.fiducial_y_entry
	fiducial_bearing_entry = application.fiducial_bearing_entry
	fiducial_edge_entry = application.fiducial_edge_entry

	# Clear out the entries just in case the deselect method was not called:
	fiducial_tag_entry.delete(0, END)
	fiducial_x_entry.delete(0, END)
	fiducial_y_entry.delete(0, END)
	fiducial_bearing_entry.delete(0, END)
	fiducial_edge_entry.delete(0, END)

	# Now fill them in:
	pi = application.pi
	fiducial_tag_entry.insert(0, str(self.id))
	fiducial_x_entry.insert(0, str(self.x))
	fiducial_y_entry.insert(0, str(self.y))
	fiducial_bearing_entry.insert(0, str(self.angle * 180.0 / pi))
	fiducial_edge_entry.insert(0, str(self.edge_length))

	# Do the final work:
	self.map_canvas.selected_tag = self
	self.color = "purple"
	self.draw()

    def show(self, label = ""):
	""" {Tag}: show contents of {self}.  """

	pi = self.map_canvas.application.pi
	print "%s Tag %d: x=%f y=%f angle=%f" % \
	  (label, self.id, self.x, self.y, self.angle * 180.0 / pi)
	for way in self.ways.values():
	    way.show(label)

    def update(self, x, y, angle, edge_length):
	""" {Tag}: update {self} contents to conatin {x}, {y}, {angle},
	    and {edge_length}. """

	self.x = x
	self.y = y
	self.angle = angle
	self.edge_length = edge_length

    def way_lookup(self, way_id):
	""" {Tag}: return the {Way} associated with {way_id} from {self}. """

	#print "way_lookup", "tag.id=", self.id, "way_id=", way_id

	ways = self.ways
	if way_id in ways:
	    # {way_id} exists; read out {way}:
            way = ways[way_id]
	else:
	    # {way_id} does not exist; create {way} and enter it into {ways}:
	    way = Way(self, way_id)
            ways[way_id] = way

	return way


class Target:
    """ {Target} represents the target cross in the canvas. """

    def __init__(self, map_canvas):
	""" {Target}:Create {self} object containing {map_canvas}. """

	# Load up {self}:
	self.map_canvas = map_canvas
	self.line1 = -1
	self.line2 = -1
	self.update(0.0, 0.0)

    def draw(self):
	""" {Target}: Draw {self} object. """

	# Extract some values from {self}:
	map_canvas = self.map_canvas
	x = self.x
	y = self.y

	# Compute the box coordinates that will contain the target cross:
	x1 = x - 2.0
	y1 = y - 2.0
	x2 = x + 2.0
	y2 = y + 2.0
	
	# Delete any previous cross segments:
	map_canvas.delete(self.line1)
	map_canvas.delete(self.line2)

	# Draw the cross:
	self.line1 = map_canvas.line(x1, y1, x2, y2, "red")
	self.line2 = map_canvas.line(x1, y2, x2, y1, "red")

    def update(self, x, y):
	""" {Target}: Update {self} to contain {x} and {y}. """

	# Load {self} with {x} and {y}:
        self.x = x
	self.y = y


class Way:
    def __init__(self, tag, id):
	""" {Way}: Create new {Way} that contains {tag} and {id}. """

	big = 99999999.9

	# Load up {self}:
	self.angle = big
	self.color = "red"
	self.dx = big
	self.dy = big
	self.grab_release_rect = -1
	self.id = id
	self.name = None
	self.rect = -1
	self.segments = []
	self.tag = tag

	# Keep track of all {Way} objects in the {Map_Canvas} object:
	tag.map_canvas.ways.append(self)

    def clear(self):
	""" {Way}: clear {self} from associated canvas: """

    	self.tag.map_canvas.delete(self.rect)

    def deselect(self):
	""" {Way}: set color of {self} to deselected. """

	self.tag.map_canvas.selected_way = None
	self.color = "red"

    def delete(self):
	""" {Way}: delete {self} from associated data structures. """

	# Remove all of the {segments}:
	segments = self.segments
	# Using a FOR loop did not work, since {Segment.delete}() modifies
	# {segments} as it does its work.  So, we always grab the {Segment}
	# at the front of {segments} until they are gone:
	while len(segments) > 0:
	    segment = segments[0]
	    segment.delete()

	# Remove {self} from the canvas display:
	self.clear()

	# Remove {self} from parent {tag}:
	tag = self.tag
	del tag.ways[self.id]

	# Let host now that {self} has been deleted:
	arguments = "{0} {1}".format(tag.id, self.id)
	tag.map_canvas.application.host_send("D", arguments)

    def draw(self):
	""" {Way}: draw {self} on associated canvas.  """

	#print "Way.draw:", "tag_id=", self.tag.id, "id=", self.id

	# Fetch the rectangle associated with {self}:
	tag = self.tag
	map_canvas = tag.map_canvas

	# Delete {rect}:
	map_canvas.delete(self.rect)

	map_canvas.delete(self.grab_release_rect)

	# Draw grab/release rectangle if needed:
	x_center = tag.x + self.dx
	y_center = tag.y + self.dy
	color = None
	if self == map_canvas.grab_way:
	    color = "yellow"
	elif self == map_canvas.release_way:
	    color = "purple"	    
	if color != None:
            self.grab_release_rect = \
	      map_canvas.rectangle(x_center, y_center, 3, 3, color)

	# Create a new {rect} for the {self}.
	self.rect = map_canvas.rectangle(x_center, y_center, 2, 2, self.color)

	# Make sure all of the segments are redrawn:
	for segment in self.segments:
	    segment.draw()

    def gui_clear(self):
	""" {Way}: Clear way values in the GUI. """

	# Get {application} from {self}:
	tag = self.tag
	map_canvas = tag.map_canvas
	application = map_canvas.application

	# Clear out the way fields in the GUI:
	application.way_height_entry.delete(0, END)
	application.way_name_entry.delete(0, END)
	application.way_open_width_entry.delete(0, END)
	application.way_close_width_entry.delete(0, END)
	application.way_flags_entry.delete(0, END)

    def gui_read(self):
	""" {Way}: Read the values from the GUI into {self}.  {True} is
	    returned if anything changed. """

	# Grab {application} out of {self}:
	application = self.tag.map_canvas.application

	# Read the value from the GUI
	close_width = float(application.way_close_width_entry.get())
	flags = application.way_flags_entry.get()
	height = float(application.way_height_entry.get())
	name = application.way_name_entry.get()
	open_width = float(application.way_open_width_entry.get())

	changed =  name != self.name or height != self.height or \
	  open_width != self.open_width or close_width != self.close_width or \
	  flags != self.flags

	# Load values into {self}:
	self.close_width = close_width
	self.flags = flags
	self.height = height
	self.name = name
	self.open_width = open_width

	# Make sure that we have a visible {Way} name:
	changed = changed or self.name_create()

	return changed

    def gui_write(self):
	""" {Way}: Write the values from {self} into the GUI. """

	# Clear out the previous values
	self.gui_clear()

	# Grab {application} from {self}:
	application = self.tag.map_canvas.application

	# Load the values from {self} into {application}:
	application.way_height_entry.insert(0, "{0}".format(self.height))
	application.way_name_entry.insert(0, "{0}".format(self.name))
	application.way_open_width_entry.insert(0, \
	  "{0}".format(self.open_width))
	application.way_close_width_entry.insert(0, \
	  "{0}".format(self.close_width))
	application.way_flags_entry.insert(0, "{0}".format(self.flags))

    def name_create(self):
	""" {Way}: Force {self} to have a name.  {True} is returned
	    if the name of {self} is changed. """

	changed = False
	if self.name == None or self.name == "":
            # Create a {Way} name:
	    self.name = "{0}{1}". \
	      format(self.tag.id, "abcdefghijklmnopqrstuvwxyz"[self.id])
	    changed = True
	return changed

    def pair(self, way2, host_notify):
	""" {Way}: Return a {Segment} binding between {self} and {way2}. """

	# Extract some values from {way1} (i.e. {self}) and {way2}:
	way1 = self
	tag1 = way1.tag
	tag2 = way2.tag
	segments1 = way1.segments
	segments2 = way2.segments

	# Lookup the segment between {way1} and {way2}:
	map_canvas = tag1.map_canvas
	segment = map_canvas.segment_lookup(way1, way2, label = "pair")

	if segment.deleted:
	    segment.deleted = False

	    # If {segment} is being created, let host know:
	    if host_notify:
		arguments = "{0} {1} {2} {3}". \
		  format(tag1.id, way1.id, tag2.id, way2.id)
       		tag1.map_canvas.application.host_send("S", arguments)

	    # {segment} now exists:
	    if way1 in segments2:
		print "pair: way1 already in segments2"
	    else:
		segments2.append(segment)
	    if way2 in segments1:
		print "pair: way2 already in segments1"
	    else:
		segments1.append(segment)
	else:
	    print "pair: segement already exists"

	return segment

    def select(self):
	""" {Way}: set {self} color to selected. """

	# Selected way has a different color:
	self.tag.map_canvas.selected_way = self
	self.color = "cyan"
	self.name_create()

	# Update the GUI:
	self.gui_write()

    def show(self, label = ""):
	""" {Way}: show contents of {self}. """

	pi = self.tag.map_canvas.application.pi
	print '  %s Way (%d %d) dx=%f dy=%f ang=%f nm="%s" clr=%s rct=%d' % \
	  (label, self.tag.id, self.id, self.dx, self.dy, \
	  self.angle * 180.0 / pi, self.name, self.color, self.rect)

	for segment in self.segments:
	    segment.show(label)

    def update(self, dx, dy, angle, name, height, \
      open_width, close_width, flags, host_notify = True):
	""" {Way}: update {self} to contain {dx}, {dy}, and {angle}. """

	# See if anything changed:
	if self.dx != dx or self.dy != dy or self.angle != angle or \
	  self.name != name or name == "" or self.height != height or \
	  self.open_width != open_width or self.close_width != close_width or \
	  self.flags != flags:
	    # Yes, load up {self}:
	    self.dx = dx
	    self.dy = dy
	    self.angle = angle
	    self.name = name
	    self.height = height
	    self.open_width = open_width
	    self.close_width = close_width
	    self.flags = flags

	    # Make sure {self.name} is non-empty
	    self.name_create()

	    # Now let host know what changed:
	    if host_notify:
		self.send()

    def send(self):
	""" {Way}: Send {self} to down to host. """

	# Grab some values starting from {self}:
	tag = self.tag
	application = tag.map_canvas.application
	pi = application.pi

	# Send {message} down to the host:
	arguments ='{0} {1} {2} {3} {4} "{5}" {6} {7} {8} "{9}"'. \
	  format(tag.id, self.id, self.dx, self.dy, \
	  self.angle * 180.0 / application.pi, self.name, \
	  self.height, self.open_width, self.close_width, self.flags)
	application.host_send("W", arguments)

	# Debugging:
	print "G:G2H: way message={0}".format(arguments)

app = Application()
app.master.title("Sample application")
app.mainloop()
