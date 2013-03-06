#!/usr/bin/octave -qf

#printf("Hello\n");
bearing_error = csvread("/tmp/BearErr.csv");
camera_bearing = csvread("/tmp/CamBear.csv");
camera_ticks = csvread("/tmp/EncTick.csv");
camera_x = csvread("/tmp/CamX.csv");
camera_y = csvread("/tmp/CamY.csv");
destination_ticks = csvread("/tmp/DstTick.csv");
enable = csvread("/tmp/Enable.csv");
encoders_bearing = csvread("/tmp/EncBear.csv");
encoders_ticks = csvread("/tmp/EncTick.csv");
encoders_x = csvread("/tmp/EncX.csv");
encoders_y = csvread("/tmp/EncY.csv");
left_position = csvread("/tmp/LeftPos.csv") / 10.0;
left_force = csvread("/tmp/LeftFrc.csv");
lift_position = max(0.0, csvread("/tmp/LiftPos.csv") - 300.0);
right_force = csvread("/tmp/RiteFrc.csv");
right_position = csvread("/tmp/RitePos.csv")/ 10.0;
speed = csvread("/tmp/Speed.csv");
target_bearing = csvread("/tmp/TarBear.csv");
target_distance = csvread("/tmp/TarDist.csv");
time = csvread("/tmp/Time.csv");
twist = csvread("/tmp/Twist.csv");

subplots = 6;

subplot(subplots, 1, 1);
plot(time, encoders_ticks, ";EncTick;",
  time, camera_ticks, ";CamTick;",
  time, left_position, ";LeftPos;",
  time, lift_position, ";LiftPos;",
  time, right_position, ";RitePos;",
  time, enable, ";Enable;")

subplot(subplots, 1, 2);
plot(time, camera_bearing, ";CamBear;",
  time, encoders_bearing, ";EncBear;",
  time, target_bearing, "g;TarBear;");
#  time, bearing_error, ";BearErr;");

subplot(subplots, 1, 3);
plot(time, speed, ";Speed;",
  time, twist, ";Twist;");

subplot(subplots, 1, 4);
plot(time, target_distance, ";TarDist;",
  time, destination_ticks, ";DstTick;")

subplot(subplots, 1, 5);
plot(time, bearing_error, "r;BearErr;",
  time, target_bearing, ";TarBear;",
  time, enable, ";Enable;")

subplot(subplots, 1, 6);
plot(time, left_force, "r;LeftFrc;",
  time, right_force, ";RiteFrc;")


print("foo.svg", "-dsvg", "-S1500,1000");

figure()
plot(camera_x, camera_y, ";CamX/Y;",
  encoders_x, encoders_y, ";EncX/Y;")
print("bar.svg", "-dsvg")

