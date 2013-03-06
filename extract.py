#!/usr/bin/python

def main():
    """  The main program. """

    log_stream = open("foo.log", "r")
 
    lifter_stream = open("/tmp/Lifter.csv", "w")

    location = {}
    data_streams = {}
    names = []

    bearing_error = 0.0
    camera_bearing = 0.0
    camera_ticks = 0
    camera_x = 0.0
    camera_y = 0.0
    destination_ticks = 0
    enable = 0.0
    encoders_bearing = 0.0
    encoders_ticks = 0
    encoders_x = 0.0
    encoders_y = 0.0
    left_force = 0.0
    left_position = 0.0
    lifter_position = 0.0
    right_force = 0.0
    right_position = 0.0
    speed = 0.0
    target_bearing = 0.0
    target_distance = 0.0
    target_x = 0.0
    target_y = 0.0
    twist = 0.0

    first_line = True
    for log_line in log_stream:
	line_values = log_line.split(' ')
	line_tag = line_values[0]
	if line_tag in "CDL":
	    line_time = float(line_values[1]) / 1000000.0
            if line_tag == "C":
		# Camera {id} {x} {y} {bearing}
		camera_ticks = (camera_ticks + 1) % 96

		camera_id = int(line_values[2])
		camera_x = float(line_values[3])
		camera_y = float(line_values[4])
		camera_bearing = float(line_values[5])
            elif line_tag == "L":
		# Encoders ....
		encoders_ticks = (encoders_ticks + 1) % 96

		# Bearing error correct should be occuring Host_Control:
		for line_value in line_values:
                    if ':' in line_value:
			pair = line_value.split(':')
			location[pair[0]] = pair[1]
		enable = float(location["En"])
		encoders_x = float(location["X"])
		encoders_y = float(location["Y"])
		encoders_bearing = max(min(float(location["B"]), 360.0), -360.0)
		target_bearing = max(min(float(location["TB"]), 360.0), -360.0)
		target_distance = float(location["TD"])
		bearing_error = max(min(float(location["BE"]), 360.0), -360.0)
		left_force = min(float(location["LF"]), 1024)
		left_position = min(float(location["LP"]), 1024.0)
		lifter_position = min(float(location["H"]), 1024.0)
		right_force = min(float(location["RF"]), 1024.0)
		right_position = min(float(location["RP"]), 1024.0)
		speed = min(float(location["S"]), 300.0)
		twist = max(min(float(location["T"]), 50.0), -50.0)

		if bearing_error > 180.0:
		    bearing_error -= 360.0
		elif bearing_error < -180.0:
                    bearing_error += 360.0
	    elif line_tag == "D":
		destination_ticks = (destination_ticks + 8) % 96

	    triples = []
            triples.append( ["BearErr", bearing_error, "{0:.1f}" ] )
            triples.append( ["CamBear", camera_bearing, "{0:.1f}" ] )
	    triples.append( ["CamTick", camera_ticks, "{0}" ] )
            triples.append( ["CamX", camera_x, "{0:.1f}" ] )
            triples.append( ["CamY", camera_y,  "{0:.1f}" ] )
            triples.append( ["Enable", enable, "{0:.1f}" ] )
            triples.append( ["EncBear", camera_bearing, "{0:.1f}" ] )
            triples.append( ["EncTick", encoders_ticks, "{0}" ] )
            triples.append( ["EncX", encoders_x, "{0:.1f}" ] )
            triples.append( ["EncY", encoders_y,  "{0:.1f}" ] )
            triples.append( ["DstTick", destination_ticks, "{0}" ] )
	    triples.append( ["LeftFrc", left_force, "{0}" ] )
	    triples.append( ["LeftPos", left_position, "{0}" ] )
	    triples.append( ["LiftPos", lifter_position, "{0}" ] )
	    triples.append( ["RiteFrc", right_force, "{0}" ] )
	    triples.append( ["RitePos", right_position, "{0}" ] )
            triples.append( ["Speed", speed, "{0:.1f}" ] )
            triples.append( ["TarDist", target_distance, "{0:.1f}" ] )
            triples.append( ["TarBear", target_bearing, "{0:.1f}" ] )
            triples.append( ["Time", line_time, "{0:.3f}"] )
            triples.append( ["Twist", twist, "{0:.1f}" ] )

	    lifter_stream.write("{0}\t{1}\n".format(line_time, lifter_position))

	    # Open all the files:
	    if first_line:
		first_line = False
		for triple in triples:
		    name = triple[0]	
                    names.append(name)
                    file_name = "/tmp/" + name + ".csv"
		    data_stream = open(file_name, "w")
		    data_streams[name] = data_stream

	    # Output the data:
	    for triple in triples:
		name = triple[0]
		data_stream = data_streams[name]
		data_stream.write(triple[2].format(triple[1]))
		data_stream.write("\n")

    # Close all I/O streams:
    for name in names:
	data_stream = data_streams[name]
	data_stream.close()
    log_stream.close()
    lifter_stream.close()

main()
