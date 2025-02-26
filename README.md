# AdaptiveAuthentication
The Adaptive Authentication project provides an automated tool to select security controls that minimize security risks and satisfy security and other requirements such as usability and performance.
We use a Fuzzy Causal Network (FCN) encoded using Z3 SMT solver to reason about the impact of contextual factors on security risks and requirements priorities and select an effective
authentication method that can be applied in the given context.

In this repository, we demonstrate our tool using an example from the Internet of Vehicles (IoVs). The IoV network is a heterogeneous vehicular network combining inter-vehicle and intra-vehicle
networks and vehicular mobile Internet. An IoV network can include users (e.g., drivers, passengers, and pedestrians), vehicles (e.g., cars, buses) and devices (e.g., mobile devices, roadside units or RSUs). We consider 3 scenarios.

## Scenario 1
The ambulance requires real-time road traffic information to reach the hospital quickly. To achieve this aim, it
communicates with the nearest RSUs using a Vehicle-to-Roadside Units (V2R) communication topology (see Figure 1a).
However, nearby vehicles may attempt to impersonate the ambulance to obtain road traffic information illegitimately. In
this scenario, ensuring the confidentiality of traffic data and the authenticity of the communicating parties (ambulance
and RSU) takes precedence over usability and performance considerations. 
To mitigate the risk of impersonation attacks, our tool suggests to employ certificate-based authentication to authenticate the
the ambulance with the RSU.

