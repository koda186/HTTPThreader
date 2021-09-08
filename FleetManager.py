import Veh_Supply


class Dispatch(object):

    # init method or constructor
    def __init__(self, thread, route, order_id, ptype, username):
        self.dispatch_request_thread = thread
        self.veh_route = route
        self.order_id = order_id
        self.ptype = ptype
        self.username = username

    # Will handle dispatch of vehicle given delivery and payload location variables.
    def assign_inactive_vehicle(self):
        print('Inside Dispatch, obtaining Vehicle:' + '\n')
        # This data would come from the database that holds cars and their info,
        # but here are hardcoded variable for now.

        dispatch_id = self.dispatch_request_thread
        veh_route = self.veh_route
        order_id = self.order_id
        ptype = self.ptype
        username = self.username

        car = Veh_Supply.Vehicle(dispatch_id, veh_route, order_id, ptype, username)
        car_status, dispatch_id, veh_route, order_id, ptype, username = car.assign_vehicle()

        print(str(car_status))
        '''
        print('Destination: ' + self.delivery_location + '\n'
              + 'Pickup: ' + self.payload_location + '\n'
              + 'Car Make: ' + self.car_make + '\n'
              + 'Car Model: ' + self.car_model + '\n'
              + 'License Plate: ' + self.car_license + '\n'
              + 'Car Status: ' + self.car_status + '\n'
              + '\n\n')
        '''
        # THIS IS WHERE DISPATCH RECORD NEEDS TO BE ADDED TO DATABASE USING dloc AND ploc
        # AND ALTERING INFORMATION FOR AVAILABLE CARS

        return car_status, dispatch_id, veh_route, order_id, ptype, username

    # -----------------------Handles Vehicle----------------------------
    def get_vehicle_info(self):
        print('Inside getVinDestInfo:' + '\n')

        # Would query from database
        dispatch_request = self.dispatch_request_thread
        sim_route = self.veh_route
        order_id = self.order_id
        ptype = self.ptype
        username = self.username

        car = Veh_Supply.Vehicle(dispatch_request, sim_route, order_id, ptype, username)

        # get inactive Vehicle and it's information so we can then assign it a route
        request_id, vin, location, destination, status = car.get_veh_info()

        return request_id, vin, location, destination, status
