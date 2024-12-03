module IESoptAddon_Battery

using IESopt
import JuMP

function initialize!(model::JuMP.Model, config::Dict)
    config["batteries"] = get_components(model; tagged="SimpleBattery")

    # All functions are expected to return `true` if everything went well.
    return true
end

function construct_variables!(model::JuMP.Model, config::Dict)
    batteries = config["batteries"]
    T = get_T(model)

    for battery in batteries
        total_capacity = access(battery.storage.state_ub)
        battery.var.useable_capacity = JuMP.@variable(
            model,
            [t = T],
            lower_bound = 0,
            upper_bound = total_capacity,
            container = Array,  # This is important, since JuMP does not "see" that our "T" allows for arrays.
            base_name = make_base_name(battery, "useable_capacity"),
        )
    end

    return true
end

function construct_constraints!(model::JuMP.Model, config::Dict)
    batteries = config["batteries"]
    T = get_T(model)

    for battery in batteries
        state_bounds(battery)
        degradation(battery, config["degradation_perc_per_cycle"])
    end

    return true
end

function construct_objective!(model::JuMP.Model, config::Dict)
    batteries = config["batteries"]

    for battery in batteries
        # Total degradation is the difference between the initial and the final useable capacity.
        battery.exp.total_degradation = access(battery.storage.state_ub) - battery.var.useable_capacity[end]

        # Degradation cost is the total degradation times the cost per kWh degraded.
        battery.obj.degradation_cost = battery.exp.total_degradation * battery.config["cost_per_kwh_degraded"]

        # Add the degradation cost to the overall default objective.
        IESopt.add_term_to_objective!(model, "total_cost", battery.obj.degradation_cost)
    end

    return true
end

function state_bounds(battery)
    T = get_T(battery.model)
    # An alternative would be to pass the model, by changing the function to:
    # `function state_bounds(model, battery)`

    var_uc = battery.var.useable_capacity
    var_state = battery.storage.var.state

    battery.con.state_lower_bound = JuMP.@constraint(
        battery.model,
        [t = T],
        0.1 * var_uc[t] <= var_state[t],
        base_name = make_base_name(battery, "state_lower_bound"),
        container = Array,
    )

    return battery.con.state_upper_bound = JuMP.@constraint(
        battery.model,
        [t = T],
        var_state[t] <= 0.9 * var_uc[t],
        base_name = make_base_name(battery, "state_upper_bound"),
        container = Array,
    )
end

function degradation(battery, degradation_perc_per_cycle)
    T = get_T(battery.model)

    var_uc = battery.var.useable_capacity
    total_capacity = access(battery.storage.state_ub)

    utilization = (battery.charging.var.flow .+ battery.discharging.var.flow) ./ 2.0

    return battery.con.degradation = JuMP.@constraint(
        battery.model,
        [t = T],
        var_uc[t] == (
            if t == T[1]
                total_capacity
            else
                var_uc[t - 1] - utilization[t - 1] * degradation_perc_per_cycle
            end
        ),
        base_name = make_base_name(battery, "degradation"),
        container = Array,
    )
end

end
