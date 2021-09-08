# HTTPThreader
-A Vehicle Simulation using HttpServer and threading via mix-in. My original project is hosted on my bitbucket found at website below: 
### https://roberteallen.com



# Mapping Service
# Vehicle Simulator
Everything you need to know to understand the vehicle simulation process, as is.
This File contains Four parts: 
### 1) Vehicle() 
### 2) Main()
### 3) vehicle_methods.py
### 4) run.py


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## SimulatorTester.py
This file contains all functions for Vehicle called by the main during the Simulation Process, which include:

# Vehicle:
* __init__(self, vin, route)
* get_V_location(self):
* get_V_total_Route_Distance(self)
* get_V_real_time_eta(self)
* get_V_total_Route_ETA(self)
* is_V_route_complete(self)
* get_dispatched_vehicle_route_steps(self)
* send_leg_eta(self)
* send_leg_distance(self)
* reverse_geocode(self)
# Vehicle - Send Vehicle Updates:
* send_V_Complete_Route_Distance(self)
* send_V_location_update(self)
* send_V_Complete_Route_ETA(self)
* send_V_real_time_eta(self)
* send_dispatch_route_ended(self)
* update_dispatch(self)
* update_dispatch_total_eta_distance(self):
# Vehicle - Pycharm Console updates:
* print_simulator_updates(self)
* print_dispatched_vehicle_route(self)
### ----------------------------------
# Main() - Simulator Tester:
* main()
* user_input(user_choices)
* menu_except(choice)
# Main() - get Dispatch Info for Vehicle:
* send_dispatch_route(dloc)
* dispatch_vehicle(dloc)
* get_vin()
* get_route_and_vin()

# Vehicle:
The functions below are for the Vehicle

## __init__(self, vin, route)
 init function or constructor gets the Vehicle vin and route.
 
```python
def __init__(self, vin, route):
	leg_counter = 0
	leg_route_eta = 0
	leg_route_distance = 0
	complete_route_distance = 0
	complete_route_eta = 0
	step_eta_total = 0
	calculated_eta_to_destination = 0
	route_step_eta = " "
	eta_duration = " "
	veh_lat= " "
	veh_lng = " "
	veh_loc = " "
	dloc = "905 E 41st St Austin TX"
	origin = "30.2330728,-97.7580753"
	#simulator route vars
	self.vin = vin
	self.origin = origin
	self.dloc = dloc
	self.json_route = route
	#calculated vars
	self.eta_duration = eta_duration
	self.calculated_eta_to_destination = calculated_eta_to_destination
	self.step_eta_total = step_eta_total
	self.route_complete = False
	#complete route vars
	self.complete_route_eta = complete_route_eta
	self.complete_route_distance = complete_route_distance
	#leg vars
	self.leg_counter = leg_counter
	self.leg_route_eta = leg_route_eta
	self.leg_route_distance = leg_route_distance
	#step vars
	self.route_step_eta = route_step_eta
	#veh location vars
	self.veh_lat = veh_lat
	self.veh_lng = veh_lng
	self.vehicle_location = veh_loc
```

## get_V_location(self)
This function assigns vehicle lat long to dictionary during route simulation to be used to update dispatch
```python
veh_lat = self.veh_lat
veh_lng = self.veh_lng
veh_location = {
	'lat': veh_lat,
	'long': veh_lng,
	}
return veh_location
```

## get_V_Complete_Route_Distance(self)
This function gets total Vehicle distance (Vehicle origin to destination distance)
```python
json_route = self.json_route
if json_route['status'] == 'NOT_FOUND':
	print("Please enter a valid delivery address!\n")
else:
	# JSON_response comes from the database dispatch api request
	for route in json_route['routes']:
		for leg in route['legs']:
			route_distance = (leg['distance']['text'])
			route_distance = route_distance.replace(',', '')  # remove comma separation
			distance = float(route_distance.split()[0])
			self.complete_route_distance += distance
			self.complete_route_distance = float(format(self.complete_route_distance, '.2f'))
	if self.complete_route_distance is 0:
		raise Exception('Error: Vehicle has not received route!')
	return self.complete_route_distance
```

## get_V_real_time_eta(self)
This function calculates the real time eta for vehicle based on location(step) in route
```python
step_eta = int(self.eta_duration.split()[0])
self.step_eta_total += step_eta
vehicle_step_eta_total = self.step_eta_total
self.calculated_eta_to_destination = self.complete_route_eta - vehicle_step_eta_total
return self.calculated_eta_to_destination
```

## get_V_total_Route_ETA(self)
This function gets total ETA for Vehicle (Vehicle origin to destination ETA)
```python
        json_response = self.json_route
        if json_response['status'] == 'NOT_FOUND':
            print("Please enter a valid delivery address!\n")
        else:
            # JSON_response comes from the database dispatch api request
            for route in json_response['routes']:
                for leg in route['legs']:
                    for step in leg['steps']:
                        self.route_step_eta = (step['duration']['text'])
                        route_step_eta = self.route_step_eta
                        step_eta = int(route_step_eta.split()[0])
                        self.complete_route_eta += step_eta
                        self.complete_route_eta = int(format(self.complete_route_eta))
            if self.complete_route_eta is 0:
                raise Exception('Error: Vehicle has not received route!')
            return self.complete_route_eta
```

## is_V_route_complete(self)
This function checks is Vehicle route complete;true or false
```python
        route_completed = self.route_complete
        real_time_eta = self.calculated_eta_to_destination
        if real_time_eta == 0:
            route_completed = True
        return route_completed
```

## get_dispatched_vehicle_route_steps(self)
This function takes the route given from Dispatch response. It pulls route info for Vehicle to simulate route.
It also calls functions to update Dispatch and Simulator Tester Console
```python
        #Count legs to get item pickup location
        leg_counter = self.leg_counter
        json_response = self.json_route

        # JSON_response comes from the database dispatch api request
        for route in json_response['routes']:
            # ---------------Print Vehicle simulator route updates------------------------
            Vehicle.print_simulator_updates(self)
            # Vehicle sends route total distance and total eta to Dispatch if vehicle assigned to route
            if self.vin != "NO VEHICLE ASSIGNED":
                Vehicle.update_dispatch_total_eta_distance(self)

            for leg in route['legs']:
                leg_counter += 1
                self.leg_route_eta = (leg['duration']['text'])
                self.leg_route_distance = (leg['distance']['text'])
                if leg_counter == 1:
                    print('First Leg of trip (Origin to Warehouse(Payload Pickup)) ETA: ' + str(Vehicle.send_leg_eta(self))
                          + ' and Distance: ' + Vehicle.send_leg_distance(self) + '\n'
                            + 'Vehicle: ' + self.vin + ' En Route' + '\n\n')
                else:
                    print('Vehicle Receiving Payload -- Vehicle Enroute: Second leg of trip (Warehouse to Destination(Delivery Address)) ETA: '
                            + str(Vehicle.send_leg_eta(self))
                            + ' and Distance: ' + str(Vehicle.send_leg_distance(self)))
                    # simulate vehicle stopped for item pickup from warehouse
                    time.sleep(5)
                    print('Vehicle: ' + self.vin + ' En Route' + '\n\n')
                for step in leg['steps']:
                    self.eta_duration = str(step['duration']['text'])
                    self.dloc = (step['end_location'])
                    self.origin = (step['start_location'])
                    # update vehicle location
                    self.veh_lat = str(step['end_location']['lat'])
                    self.veh_lng = str(step['end_location']['lng'])
                    time.sleep(7)

                    # Print route to console to simulate vehicle traversing route
                    Vehicle.print_dispatched_vehicle_route(self)
                    # send real time updates and confirmation route ended  to dispatch if vehicle assigned to route:
                    if self.vin != "NO VEHICLE ASSIGNED":
                        Vehicle.update_dispatch(self)
```

## send_leg_eta(self)
This function gets each "leg of route" ETA
Legs for "RENT'D AND Farm to Home" are "Origin to Payload pickup" and "Payload pickup to destination"
```python
        leg_route_eta = self.leg_route_eta
        leg_route_eta = json.dumps(leg_route_eta)
        return leg_route_eta
```

## send_leg_distance(self)
This function gets each "leg of route" distance
Legs for "RENT'D AND Farm to Home" are "Origin to Payload pickup" and "Payload pickup to destination"
```python
        leg_route_distance = self.leg_route_distance
        leg_route_distance = json.dumps(leg_route_distance)
        return leg_route_distance
```

## reverse_geocode(self)
This function gets the address from Dispatched route that google maps auto-corrected from user input
Functionality: if user enters ausitn, Tx; Google Maps auto-corrects and suspects user meant Austin,TX
```python
        #Count legs to get item pickup location
        leg_counter = 0
        json_response = self.json_route
        # test to see if the request was valid
        if json_response['status'] == 'NOT_FOUND':
            print("Please enter a valid delivery address!\n")
        else:
            for route in json_response['routes']:
                for leg in route['legs']:
                    leg_counter += 1
                    end_address = (leg['end_address'])
                    if leg_counter == 2:
                        return str(end_address)
```

# Vehicle - Send Vehicle Updates:
The functions below send vehicle updates to Dispatch

## update_dispatch(self)
This function calls other functions to update Dispatch on Vehicle route information
```python
        # --------------Vehicle sends location update to Dispatch---------------
        Vehicle.send_V_location_update(self)
        #--------------Vehicle sends real time eta update to Dispatch---------------
        Vehicle.send_real_time_eta(self)
        #--------------Vehicle sends "is route complete" comfirmation to Dispatch-----
        Vehicle.send_dispatch_route_ended(self)
```

## update_dispatch_total_eta_distance(self)
Vehicle sends route total distance and total eta to Dispatch
```python
        # --------Vehicle sends route total distance to Dispatch---------------
        Vehicle.send_V_Complete_Route_Distance(self)
        # --------Vehicle sends total route eta to Dispatch -------------------
        Vehicle.send_V_Complete_Route_ETA(self)
```

## send_V_Complete_Route_Distance(self)
This function sends (Total) route distance to Dispatch
```python
        complete_route_distance = self.complete_route_distance

        total_distance = {
            'distance': str(complete_route_distance)
        }

        url = "https://team12.supply.softwareengineeringii.com/supply/updateV_Complete_Route_Distance"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(total_distance), headers=headers)
```

## send_V_location_update(self)
This function sends dispatch the VIN and real time Vehicle location updates as it routes to destination
```python
        vehicle_location = Vehicle.get_V_location(self)
        url = "https://team12.supply.softwareengineeringii.com/supply/updateV_Location"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(vehicle_location), headers=headers)
```

## send_V_Complete_Route_ETA(self)
This function sends (total) route eta to Dispatch
```python
        complete_route_eta = self.complete_route_eta
        vin = self.vin

        total_eta = {
            'vin': vin,
            'compETA': str(complete_route_eta)
        }

        url = "https://team12.supply.softwareengineeringii.com/supply/updateV_Complete_Route_ETA"
        #complete_route_eta = self.complete_route_eta
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(total_eta), headers=headers)
```

## send_V_real_time_eta(self)
This function sends dispatch real time ETA updates from vehicle as it routes to destination
```python
        vehicle_real_time_eta = self.calculated_eta_to_destination
        vin = self.vin

        current_ETA = {
            'vin': vin,
            'currETA': str(vehicle_real_time_eta)
        }
        url = "https://team12.supply.softwareengineeringii.com/supply/updateV_Real_Time_ETA"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(current_ETA), headers=headers)
```

## send_dispatch_route_ended(self)
This function sends dispatch update "is route complete"; True: Vehicle route complete || False: Vehicle route incomplete
```python
        vin = self.vin
        dispatch_conf = {
            'vin': vin,
            'routeBool': str(Vehicle.is_V_route_complete(self))
        }
        url = "https://team12.supply.softwareengineeringii.com/supply/updateV_Is_Route_Complete"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(dispatch_conf), headers=headers)
```

# Vehicle - Pycharm Console updates:
The functions below print to PyCharm Console for Simulator Tester

## print_simulator_updates(self)
This function updates Simulator Tester PyCharm console so user can know Vehicel route information
```python
        veh_vin = self.vin
        print('\n\n' + 'You chose Destination Address: ' + str(Vehicle.reverse_geocode(self)))
        print('Vehicle Dispatched: VIN of Vehicle IN SERVICE: ' + veh_vin)
        print('Route Calculated: Distance of Trip: ' + str(Vehicle.get_V_Complete_Route_Distance(self)) + ' miles')
        print('ETA to destination: ' + str(Vehicle.get_V_total_Route_ETA(self)) + ' minutes')
```

## print_dispatched_vehicle_route(self)
This function updates Simulator Tester PyCharm console so user can know Vehicel route information
```python
        origin = self.origin
        dloc = self.dloc
        veh_vin = self.vin
        # print route steps
        print('Inside Dispatch -- VEHICLE DISPATCH REPORT FOLLOWS: ' + '\n'
              + 'CURRENT vehicle VIN: ' + veh_vin + '\n' + 'Vehicle origin: ' + str(origin)
              + ' TRAVELLING to next step of Vehicle destination: ' + str(dloc)
              + '\n' + 'Updated Vehicle location in Dispatch: ' + str(Vehicle.get_V_location(self))
              + '\n' + 'Vehicle Real Time ETA to destination: ' + str(Vehicle.get_V_real_time_eta(self)) + ' minutes away'
              + '\n' + 'Vehicle Reports Route Complete: ' + str(Vehicle.is_V_route_complete(self))
              + '\n\n')
        if Vehicle.is_V_route_complete(self):
            print('Vehicle Arrived at Destination: Dispatch confirmation sent')
        else:
            print('Vehicle: ' + veh_vin + ' En Route')
```

# Main() - Simulator Tester:
The functions below are to test User input for Simulator

## Main()
Allows user to choose options to test Vehicle Simulator
```python
    test_cases = {1: 'To test the ROUTE of a vehicle simulator to Destination Address of: 3001 Congress St, Austin TX 78704',
                  2: 'To test the ROUTE of a vehicle simulator to destination of your choice. Please use following format: 3001 Congress St, Austin TX 78704',
                  3: 'To test the ROUTE of a vehicle simulator to Destination Address of Invalid Input: dddd yyry',
                  4: 'To SIMULATE VEHICLE DRIVING to following Destination Address while also updating Dispatch: 905 E 41st St Austin TX 78751',
                  5: 'To SIMULATE VEHICLE DRIVING to Destination Address of your choice while also updating Dispatch. Please enter address with following format: 3001 Congress St, Austin TX 78704',
                  6: 'To SIMULATE VEHICLE DRIVING to Destination Address of Invalid Input: 223 Djak Sdsf',
                  7: 'Simulate Dispatch connection: Show Vin and Route of open record',
                  8: 'Test Vehicle REST API to dispatch vehicle',
                  9: 'Future',
                  10: 'Exit this menu'}
```

## user_input(user_choices)
This function Maps user console input to a test case
UserChoices is a dictionary, key points to test case
Includes user input exception handling
Loop until user input is '10'
```python
        while True:
            print(' your choices'.upper(), '\t\t\tTest Case\n'.upper(), '-' * 55)

            for key, value in user_choices.items():
                print('\t', key, ' \t\t\t\t', value)
            try:
                choice = int(input("\nPlease enter the numeric choice for a Test Case \n\t --> ".upper()))
            except:
                print("\nSomething went wrong, please enter a numeric value!!!\n")
                continue

            if choice == 10:
                break

            menu_except(choice)
```

## menu_except(choice)
This function takes numeric choice for Test Case above
Maps user menu selection (parameter) to module (function call)
```python
        # testCases
        test_route_only_empty_veh_vin = "NO VEHICLE ASSIGNED"
        test_route_dloc = "3001 Congress St, Austin TX 78704"
        test_route_invalid_addr = "dddd yyry"
        test_V_dloc = "905 E 41st St Austin TX"
        test_V_invalid_addr = "223 Djak Sdsf"

        if choice == 1:
            # print('You chose: ' + str(test_route_dloc))
            response = dispatch_vehicle(test_route_dloc)
            # give vehicle route and empty vin
            car = Vehicle(test_route_only_empty_veh_vin, response)
            #test route
            car.get_dispatched_vehicle_route_steps()
        elif choice == 2:
            test_route_dloc_input = input('\tPlease enter a Delivery Address --> ')
            print('You chose: ' + str(test_route_dloc_input))
            response = dispatch_vehicle(test_route_dloc_input)
            # give vehicle route and empty vin
            car = Vehicle(test_route_only_empty_veh_vin, response)
            #test route
            car.get_dispatched_vehicle_route_steps()
        elif choice == 3:
            print('You chose: ' + str(test_route_invalid_addr))
            response = dispatch_vehicle(test_route_invalid_addr)
            # give vehicle route and empty vin
            car = Vehicle(test_route_only_empty_veh_vin, response)
            #test route
            car.get_dispatched_vehicle_route_steps()
        elif choice == 4:
            print('You chose: ' + str(test_V_dloc))
            response = dispatch_vehicle(test_V_dloc)
            if response['status'] != 'NOT_FOUND':
                # request creation of open dispatch record order
                request_V_dispatch_open_record(test_V_dloc)
                # get available vehicle
                vin = get_vin()
                # assign vehicle route
                car = Vehicle(vin, response)
                # dispatch vehicle
                car.get_dispatched_vehicle_route_steps()
        elif choice == 5:
            test_V_dloc_input = input('\tPlease enter a Delivery Address --> ')
            print('You chose: ' + str(test_V_dloc_input))
            response = dispatch_vehicle(test_V_dloc_input)
            # request creation of open dispatch record order
            if response['status'] != 'NOT_FOUND':
                request_V_dispatch_open_record(test_V_dloc_input)
                # get available vehicle
                vin = get_vin()
                # assign vehicle route
                car = Vehicle(vin, response)
                # dispatch vehicle
                car.get_dispatched_vehicle_route_steps()
        elif choice == 6:
            print('You chose: ' + str(test_V_invalid_addr))
            response = dispatch_vehicle(test_V_invalid_addr)
            if response['status'] != 'NOT_FOUND':
                # request creation of open dispatch record order
                request_V_dispatch_open_record(test_V_invalid_addr)
                # get available vehicle
                vin = get_vin()
                # assign vehicle route
                car = Vehicle(vin, response)
                # dispatch vehicle
                car.get_dispatched_vehicle_route_steps()
        elif choice == 7:
            print('Retrieving Dispatch open record: Vehicle vin and route follows:')
            # request creation of open dispatch record order
            request_V_dispatch_open_record(test_V_dloc)
            # get open record from dispatch
            vin, response = get_route_and_vin()
            # assign vehicle route
            car = Vehicle(vin, response)
            # dispatch vehicle
            car.get_dispatched_vehicle_route_steps()
        elif choice == 8:
            print('You are testing the Vehicle REST API to dispatch vehicle')
            print('Check Dispatch database for Vehicle updates')
            test_vehicle_api()
        elif choice == 9:
            print('test case construction underway, come back soon!')
        else:
            print('What you talking about Willis? Please try a valid choice!')

        input('*************** Press Enter to continue ******************\n\n'.upper())
```

# Main() - get Dispatch Info for Vehicle:
The funtions below are apart of "Main()". Thye make requests to Dispatch to get Vehicle route information. 

## send_dispatch_route(dloc)
For simulation purposes: Dispatch needs route from User input, It is put into a dictionary
```python
        # a Python object (dict):
        dispatch_info = {
            'origin': '30.23001039999999, -97.75471589999999',
            'ploc': '314 West 11th St Austin TX 78701',
            'dloc': dloc
        }
        return dispatch_info
```
## dispatch_vehicle(dloc)
This function is a request to dispatch
The request url "/supply/testRoute" takes the dispatch_info given from Simulator Tester Pycharm Console
In return the Tester receives a route with 'step by step' instructions for Vehicle so we can run route testcases.
```python
        url = "https://team12.supply.softwareengineeringii.com/supply/testRoute"
        dispatch_info = send_dispatch_route(dloc)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(dispatch_info), headers=headers)

        #get vin of vehicle dispatched
        vin = get_vin()
        output = r.json()
        if r.status_code == 200:
            output = r.json()
        else:
            print('Not a valid request path.\n')

        # test to see if the request was valid
        if output['status'] == 'NOT_FOUND':
            print("Invalid delivery address input: " + dloc + "\n" + "Please try again! \n")
            user_input(test_cases)
        else:
            return vin, output
```

## request_V_dispatch_open_record(dloc)
create open record in dispatch to test vehicle simulating route given
```python
        # randrange only output integers
        order_id = random.randrange(100, 1001)

        open_record = {
            'orderID': order_id,
            'ptype': 'clothes',
            'dloc': dloc,
            'ploc': '9500 S IH 35 Frontage Rd Ste H, Austin',
            'username': 'simulatorTester'
        }

        url = "https://team12.supply.softwareengineeringii.com/supply/requestv"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(open_record), headers=headers)
        print(r.status_code)
```

## get_vin()
Notifies Tester which vehicle will be used
```python
        http = "https://team12.supply.softwareengineeringii.com/supply/testDispatch"
        r = requests.get(url=http)
        binary = r.content
        dispatch_Info = json.loads(binary)
        VIN = dispatch_Info.get('vin')
        return VIN
```

## get_route_and_vin()
This method simply fetches a route that has already been created and placed into an existing and open Dispatch Record, along with it's corresponding VIN.
```python
        http = "https://team12.supply.softwareengineeringii.com/supply/testDispatch"
        r = requests.get(url=http)
        binary = r.content
        dispatch_Info = json.loads(binary)
        VIN = dispatch_Info.get('vin')
        route = dispatch_Info.get('route')
        return VIN, route
```

## test_vehicle_api()
test Vehicle REST api
```python
    def test_vehicle_api():
        http = "https://team12.supply.softwareengineeringii.com/mapping/requestSimDispatch_V"
        r = requests.get(url=http)
        print(r.status_code)
```

# vehicle_methods.py
contains the methods for run.py

## parse_post_path(path)
parse the post request from run.py
```python
    #@staticmethod
        print('Inside parsePostPath:' + '\n')

        path_parse = parse.urlparse(path)
        i = 0
        while path_parse[i]:
            print('Result of path parse at i: ' + path_parse[i] + ' ' + i.__str__() + '\n')
            i += 1
        path = path_parse[2]
        print('Path of url: ' + path + '\n\n')
        if path != "/mapping/postTest":
            raise Exception("Not a valid request path.")
        return path
```

## parse_get_path(path)
parse the get request
```python
    #@staticmethod
        print('Inside parseGetPath:' + '\n')

        path_parse = parse.urlparse(path)
        i = 0
        while path_parse[i]:
            print('Result of path parse at i: ' + path_parse[i] + ' ' + i.__str__() + '\n')
            i += 1
        path = path_parse[2]
        print('Path of url: ' + path + '\n\n')
        if path != "/mapping/requestV_Route" and path != "/mapping/requestDispatch_V":
            raise Exception("Not a valid request path.")
        return path
```

## get_route_and_vin()
returns dispatch route open record
testDispatch, does not require any input, looks for open dispatch record,
returns the vin of vehicle in record as well as the record route
```python
    #@staticmethod
        http = "https://team12.supply.softwareengineeringii.com/supply/testDispatch"
        r = requests.get(url=http)
        binary = r.content
        dispatch_info = json.loads(binary)
        VIN = dispatch_info.get('vin')
        route = dispatch_info.get('route')
        return VIN, route
```

## request_v_dispatch_open_record()
create open record in dispatch to test dispatch vehicle simulating with vin and route record given.
```python
    #@staticmethod
        # randrange only output integers
        order_id = random.randrange(100, 1001)
        dloc = "2706 east 22nd st, Austin,TX 78722"

        open_record = {
            'orderID': order_id,
            'ptype': 'clothes',
            'dloc': dloc,
            'ploc': '9500 S IH 35 Frontage Rd Ste H, Austin',
            'username': 'VehicleRestApi'
        }

        url = "https://team12.supply.softwareengineeringii.com/supply/requestv"
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(open_record), headers=headers)
        print(r.status_code)
```
## get_v_route()
get the vin and route from dispatch request
```python
    #@staticmethod
        vin, route = Methods.get_route_and_vin()
        return vin, route
```
## dispatch_vehicle(vin, route)
dispatch vehicle simulator
```python
    #@staticmethod
        car = simulator.simulatorTester.Vehicle(vin, route)
        car.get_dispatched_vehicle_route_steps()
```

# run.py
Any and all GET requests will reach here.
## do_GET(self)
```python
        self.send_response(200)
        self.end_headers()

        # Parsing and checking GET request Path.

        print(self.path)
        path = simulator.vehicle_methods.Methods.parse_get_path(self.path)

        if path == "/mapping/requestV_Route":

            # Path is valid. Parsing request To get Vehicle Route.
            vin, route = simulator.vehicle_methods.Methods.get_v_route()
            dispatch_info = {
                'vin': vin,
                'route': route
            }
            # Fetched route and assigned vehicle VIN. Returning values now.
            dispatch_string = json.dumps(dispatch_info)
            self.wfile.write(dispatch_string.encode(encoding='utf_8'))
        elif path == "/mapping/requestSimDispatch_V":
            # This creates an open record in dispatch so we can simulate dispatching vehicle

            # create open record for vehicle simulation
            simulator.vehicle_methods.Methods.request_v_dispatch_open_record()
            # get the vin and route from open record from making a dispatch request
            vin, route = simulator.vehicle_methods.Methods.get_v_route()
            # JSON file parsed. Simulate Dispatching Vehicle with route.
            simulator.vehicle_methods.Methods.dispatch_vehicle(vin, route)
            # Vehicle Dispatch Complete. See Database for route Info.\n\n')
        elif path == "/mapping/requestDispatch_V":
            # This takes an already created open record from dispatch and dispatches vehicle

            # get the vin and route from open record from dispatch
            vin, route = simulator.vehicle_methods.Methods.get_v_route()
            # JSON file parsed. Simulate Dispatching Vehicle with route.
            simulator.vehicle_methods.Methods.dispatch_vehicle(vin, route)
            # Vehicle Dispatch Complete. See Database for route Info.\n\n')
        else:
            self.send_response(400)
            self.wfile.write(b'Not a valid POST request path.\n\n')
```
