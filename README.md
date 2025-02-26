# AdaptiveAuthentication Project
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

## Scenario 2
In the second scenario, the ambulance attempts to overtake a car. This requires exchanging
distance information between the ambulance and nearby vehicles using a Vehicle-to-Vehicle
(V2V) communication topology. Ensuring the integrity of this distance information is critical to preventing collisions.
Also, the exchange must happen quickly to enable the ambulance to overtake the car without delay. Here,
performance requirements, such as minimizing authentication time, are prioritized over security and usability concerns.
Certificate-based authentication is unsuitable in this case, as it may involve lengthy identity verification through a remote server. Instead, our tool recommends using car plates and driver's license for authentication since they offer faster authentication while reducing the risk of impersonation attacks.

## Scenario 3
In the third scenario, the ambulance driver is approaching a junction and accessing patient information through a Vehicle-to-Infrastructure
(V2I) connection via cellular networks. Since the information is sensitive, ensuring its confidentiality is
crucial. At the same time, usability is also a key consideration, as the authentication process should not distract the
driver, who needs to remain focused on navigating the junction. Our tool recommends using two-factor authentication based on a biometrics-based authentication method combined with a car plate and driver's license since these are automated and do not require the driver to perform an action (e.g., type a password or swipe a card).

# Project Structure
| <br />
|-- adaptive_auth.py<br />
|<br />
|-- Scenario1 <br />
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     |-- model-zu-1.txt<br />
|<br />
|-- Scenario2 <br />
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;      |-- model-zu-2.txt<br />
|<br />
|-- Scenario3<br />
 &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     |-- model-zu-3.txt<br /><br />

*adaptive_auth.py* This is a bash script which computes the authentication method that provides the best utility

*model-zu-1.txt* is the Z3 model representing Scenario 1

*model-zu-2.txt* is the Z3 model representing Scenario 2

*model-zu-3.txt* is the Z3 model representing Scenario 3

# Installation Requirements
1) Install Python v3.
2) Install the Z3 theorem prover on your machine (See https://github.com/z3prover/z3).
3) Ensure that the z3 command (e.g., z3.sh or z3.exe) is in the PATH environment variable.

# Run the Adaptive Authentication Scenarios
1) Using your terminal, go to the AdaptiveAuthentication project folder.
2) To run Scenario 1-3, respectively execute commands <br />
  &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  *python adaptive_auth.py 1* <br />
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  *python adaptive_auth.py 2* <br />
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  *python adaptive_auth.py 3*
   
