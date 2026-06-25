# AdaptiveAuthentication Project
The Adaptive Authentication project provides an automated tool to select security controls that minimize security risks and satisfy security and other requirements, such as usability and performance.
We use a Fuzzy Causal Network (FCN) encoded using Z3 SMT solver to reason about the impact of contextual factors on security risks and requirements priorities, and select an effective authentication method that can be applied in the given context.

In this repository, we demonstrate our tool using a healthcare example. Healthcare information systems manage highly sensitive, safety-critical patient data across interconnected components, including electronic health records, prescription platforms, and administrative systems. These systems are accessed by multiple users with different roles, including clinicians and administrative staff, operating under dynamic conditions such as shared workstations, remote access, shift changes, and emergency situations. We consider 3 scenarios.

## Scenario 4
A family physician attempts to prescribe medication outside the hospital from an unknown location, over an insecure network, and at an unusual time. In this scenario, impersonation and session‑hijacking attacks are highly likely. Also, confidentiality and integrity of the prescribing action have higher priority than usability and performance goals. Thus, an effective authentication method shall reduce the likelihood of impersonation and session‑hijacking attacks and maximize the satisfaction of confidentiality and integrity requirements. 

## Scenario 5
A physician in the emergency department needs to quickly authenticate to access a patient’s medical records during a critical situation using a hospital tablet connected to the internal Wi-Fi network. Because the environment is crowded and devices are shared among staff, impersonation and replay attacks are likely. Due to the emergency, the performance requirement has a higher priority than the security requirements. Thus, an effective authentication method shall reduce the likelihood of impersonation and replay attacks while satisfying the most critical goals (Performance).
## Scenario 6
The physician accesses the hospital system from home at night using a personal, unmanaged laptop on an unsecured Wi‑Fi network. The device lacks a fingerprint scanner, and the smart‑card reader is unavailable. Because access occurs from an untrusted device and over an insecure connection, the risk of session hijacking is high. Therefore, the security requirement has the highest priority in this context. An effective authentication method shall reduce the likelihood of session‑hijacking (and related replay) attacks to satisfy security goals, which are the most critical in this scenario.

# Project Structure
| <br />
|-- adaptive_auth.py<br />
|<br />
|-- Scenario4 <br />
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     |-- model-zu-4.txt<br />
|<br />
|-- Scenario5 <br />
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;      |-- model-zu-5.txt<br />
|<br />
|-- Scenario6<br />
 &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;     |-- model-zu-6.txt<br /><br />

*adaptive_auth.py* This is a bash script that computes the authentication method that provides the best utility

*model-zu-4.txt* is the Z3 model representing Scenario 4

*model-zu-5.txt* is the Z3 model representing Scenario 5

*model-zu-6.txt* is the Z3 model representing Scenario 6

# Installation Requirements
1) Install Python v3.
2) Install the Z3 theorem prover on your machine (See https://github.com/z3prover/z3).
3) Ensure that the z3 command (e.g., z3.sh or z3.exe) is in the PATH environment variable.

# Run the Adaptive Authentication Scenarios
1) Using your terminal, go to the AdaptiveAuthentication project folder.
2) To run Scenario 4-6, respectively execute commands <br />
  &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  *python adaptive_auth.py 4* <br />
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  *python adaptive_auth.py 5* <br />
&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  *python adaptive_auth.py 6*
   
