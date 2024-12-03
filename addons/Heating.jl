module IESoptAddon_Heating

using IESopt
import JuMP

function initialize!(model::JuMP.Model, config::Dict)
    config["heatings"] = get_components(model; tagged="SimpleHeating")

    # All functions are expected to return `true` if everything went well.
    return true
end

function after_construct_variables!(model::JuMP.Model, config::Dict)
    for heating in config["heatings"]
        modify_heatpump(heating)
        modify_radiator(heating)
    end

    return true
end

function modify_heatpump(heating)
    model = heating.model
    T = get_T(model)

    t_hi = heating.temperature.var.value
    t_lo = heating.get_ts("t_cold")
    eta = heating.get("eta")

    heating.var.hp_out =
        JuMP.@variable(model, [t = T], base_name = make_base_name(heating, "hp_out"), container = Array)

    heating.con.set_hp_out = JuMP.@constraint(
        model,
        [t = T],
        heating.var.hp_out[t] * (t_hi - t_lo[t]) == (t_hi + 237.15) * eta * heating.heatpump.exp.in_electricity[t],
        base_name = make_base_name(heating, "set_hp_out"),
        container = Array
    )

    JuMP.add_to_expression!.(heating.heatpump.exp.out_heat, heating.var.hp_out)
    JuMP.add_to_expression!.(heating.heating_loop.exp.injection, heating.var.hp_out)

    return nothing
end

function modify_radiator(heating)
    model = heating.model
    T = get_T(model)

    t_hi = heating.temperature.var.value
    out = get_component(model, heating.get("out"))
    t_house = out.var.state

    heating.var.rad_out =
        JuMP.@variable(model, [t = T], base_name = make_base_name(heating, "rad_out"), container = Array)

    heating.con.set_rad_out = JuMP.@constraint(
        model,
        [t = T],
        heating.var.rad_out[t] * (t_hi + 237.15) == heating.radiator.exp.in_heat[t] * (t_hi - t_house[t]),
        base_name = make_base_name(heating, "set_rad_out"),
        container = Array
    )

    JuMP.add_to_expression!.(heating.radiator.exp.out_heat, heating.var.rad_out)
    JuMP.add_to_expression!.(out.exp.injection, heating.var.rad_out)

    return nothing
end

end
