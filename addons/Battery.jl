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

end
