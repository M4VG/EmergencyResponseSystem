# EmergencyResponseSystem

A multiagent intelligent system which efficiently responds to emergencies in a simulated environment.

## Usage

To perform a simulation run the following command:
```sh
python3 Main.py <agent_type> [csv_file]
```

An agent can be one out of three types:

- Reactive
- Deliberative
- Social Deliberative

> A Social Deliberative agent is a Deliberative agent capable of communicating with other agents.

The placeholder <agent_type> should be either *r* (Reactive), *d* (Deliberative), or *dc* (Deliberative w/ Communication).

The optional placeholder [csv_file] is needed if one desires to save the results of a simulation. It should be replaced with the filename of the .csv file in which the results will be stored.
