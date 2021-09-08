import random
import SimulatorTester


class Vehicle(object):

    # init method or constructor
    def __init__(self, dispatch_request, route, order_id, ptype, username):
        self.dispatch_request = dispatch_request
        self.vehicle_route = route
        status = "Inactive"
        self.status = status
        self.order_id = order_id
        self.ptype = ptype
        self.username = username
        self.vin = str(random.randrange(234568000000, 534568000000, 999))

    # We would search database for "Active" status vehicle,
    # get its location details and update its dispatch id and set status to active
    def get_veh_info(self):

        vin = str(random.randrange(234568000000, 534568000000, 999))
        location = "1509 Holly Street, Austin, TX 78722"
        destination = "2704 East 22nd Street, Austin, TX 78702"
        dispatch_thread_id = "Thread Process Request is : " + str(self.dispatch_request)
        status = "Active"

        return dispatch_thread_id, vin, location, destination, status

    def assign_vehicle(self):
        print('Inside Dispatch, Getting Vehicle Information, Then will dispatch once Vehicle is confirmed:' + '\n')

        order_id = self.order_id
        ptype = self.ptype
        username = self.username
        vin = self.vin
        route = self.vehicle_route
        dispatch_request = self.dispatch_request

        # Find inactive Vehicle in DB, set it to active
        # Update order attributes and assign vehicle to it in DB
        # Ensure Vehicle has route information
        Vehicle.status = "VIN: " + str(vin) + " is set to 'Active' status" \
                         + " for Order_id: " + str(order_id) + " with payload type " + ptype + \
                         " for client '" + username + "'/n" + "Loading Directions:" + str(route)
        print("Loading Directions")

        return Vehicle.status, dispatch_request, route, order_id, ptype, username

    def dispatch_assigned_vehicle(self):
        vin = self.vin
        route = self.vehicle_route
        dispatch_request = self.dispatch_request

        assigned_vehicle = SimulatorTester.Simulator(dispatch_request, route, vin)
        assigned_vehicle.get_dispatched_vehicle_route_steps()

        # We would set status back to inactive in DB
        return "Vehicle status set back to 'inactive'"
