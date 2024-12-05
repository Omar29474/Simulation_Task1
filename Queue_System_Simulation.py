import random

def single_queue_simulation(num_customers, max_interarrival, max_service_time):
    """Simulates a single-queue system."""
    # Generate random inter-arrival times, with the first customer's inter-arrival time as 0
    inter_arrival_times = [0] + [random.randint(1, max_interarrival) for _ in range(num_customers - 1)]
    service_times = [random.randint(1, max_service_time) for _ in range(num_customers)]

    # Initialize simulation variables
    arrival_times = [sum(inter_arrival_times[:i+1]) for i in range(num_customers)]
    service_start_times = [0] * num_customers
    service_end_times = [0] * num_customers
    waiting_times = [0] * num_customers
    idle_times = [0] * num_customers

    # customer processing
    for i in range(num_customers):
        if i == 0:
            service_start_times[i] = arrival_times[i]
            idle_times[i] = 0  # No idle time for the first customer
        else:
            idle_times[i] = max(0, arrival_times[i] - service_end_times[i - 1])
            service_start_times[i] = max(arrival_times[i], service_end_times[i - 1])

        waiting_times[i] = service_start_times[i] - arrival_times[i]
        service_end_times[i] = service_start_times[i] + service_times[i]

    # Calculations
    total_waiting_time = sum(waiting_times)
    avg_waiting_time = total_waiting_time / num_customers
    total_service_time = sum(service_times)
    total_idle_time = sum(idle_times)

    # Return results
    return {
        "Inter-Arrival Times": inter_arrival_times,
        "Service Times": service_times,
        "Arrival Times": arrival_times,
        "Time Service Begins": service_start_times,
        "Time Service Ends": service_end_times,
        "Waiting Times": waiting_times,
        "Idle Times": idle_times,
        "Average Waiting Time": avg_waiting_time,
        "Total Service Time": total_service_time,
        "Total Idle Time": total_idle_time,
    }


def multi_queue_simulation(num_customers, max_interarrival, max_service_time_able, max_service_time_baker):
    """Simulates a multi-queue system with two servers: Able and Baker."""
    # Generate random inter-arrival times, with the first customer's inter-arrival time as 0
    inter_arrival_times = [0] + [random.randint(1, max_interarrival) for _ in range(num_customers - 1)]
    service_times_able = [random.randint(1, max_service_time_able) for _ in range(num_customers)]
    service_times_baker = [random.randint(1, max_service_time_baker) for _ in range(num_customers)]

    # Initialize simulation variables
    arrival_times = [sum(inter_arrival_times[:i+1]) for i in range(num_customers)]
    service_start_times = [0] * num_customers
    service_end_times = [0] * num_customers
    waiting_times = [0] * num_customers
    idle_times = [0] * num_customers
    server_assignment = [""] * num_customers

    # Initialize server completion times
    able_service_completion = 0
    baker_service_completion = 0

    # customer processing
    for i in range(num_customers):
        if able_service_completion <= arrival_times[i] and baker_service_completion <= arrival_times[i]:
            # Both servers are idle, assign to Able
            server_assignment[i] = "Able"
            idle_times[i] = arrival_times[i] - max(able_service_completion, baker_service_completion)
            service_start_times[i] = arrival_times[i]
            service_end_times[i] = service_start_times[i] + service_times_able[i]
            able_service_completion = service_end_times[i]
        elif able_service_completion <= baker_service_completion:
            # Assign to Able
            server_assignment[i] = "Able" 
            idle_times[i] = max(0, arrival_times[i] - able_service_completion)
            service_start_times[i] = max(arrival_times[i], able_service_completion)
            service_end_times[i] = service_start_times[i] + service_times_able[i]
            able_service_completion = service_end_times[i]
        else:
            # Assign to Baker
            server_assignment[i] = "Baker"
            idle_times[i] = max(0, arrival_times[i] - baker_service_completion)
            service_start_times[i] = max(arrival_times[i], baker_service_completion)
            service_end_times[i] = service_start_times[i] + service_times_baker[i]
            baker_service_completion = service_end_times[i]

        waiting_times[i] = service_start_times[i] - arrival_times[i]

    # Calculations
    total_waiting_time = sum(waiting_times)
    avg_waiting_time = total_waiting_time / num_customers
    total_service_time_able = sum([service_times_able[i] for i in range(num_customers) if server_assignment[i] == "Able"])
    total_service_time_baker = sum([service_times_baker[i] for i in range(num_customers) if server_assignment[i] == "Baker"])
    total_idle_time = sum(idle_times)

    # Return results
    return {
        "Inter-Arrival Times": inter_arrival_times,
        "Service Times Able": service_times_able,
        "Service Times Baker": service_times_baker,
        "Arrival Times": arrival_times,
        "Time Service Begins": service_start_times,
        "Time Service Ends": service_end_times,
        "Waiting Times": waiting_times,
        "Idle Times": idle_times,
        "Server Assignments": server_assignment,
        "Average Waiting Time": avg_waiting_time,
        "Total Service Time Able": total_service_time_able,
        "Total Service Time Baker": total_service_time_baker,
        "Total Idle Time": total_idle_time,
    }


# Example usage
if __name__ == "__main__":
    single_queue_results = single_queue_simulation(num_customers=20, max_interarrival=8, max_service_time=6)
    print("Single Queue Simulation Results:")
    for key, value in single_queue_results.items():
        print(f"{key}: {value}")
        
         
    multi_queue_results = multi_queue_simulation(
        num_customers=20, 
        max_interarrival=5, 
        max_service_time_able=5, 
        max_service_time_baker=7
    )
    print("\nMulti-Queue Simulation Results:")
    for key, value in multi_queue_results.items():
        print(f"{key}: {value}")
