Prelude
=======

Prelude is a Universal "Security Information & Event Management" (SIEM) system.
Prelude collects, normalizes, sorts, aggregates, correlates and reports all
security-related events independently of the product brand or license giving
rise to such events; Prelude is "agentless".

As well as being capable of recovering any type of log (system logs, syslog,
flat files, etc.), Prelude benefits from a native support with a number of
systems dedicated to enriching information even further (snort, samhain, ossec,
auditd, etc.).

Prelude standardizes all the notables or suspicious events to `IDMEF`_
standard format (RFC 4765). With this format, events are enriched to facilitate
automation and correlation processes but also to provide as much information to
the operator (contextualization alerts) to allow it to respond quickly and
effectively.

Libprelude is a collection of generic functions providing communication between
all Sensors, like IDS (Intrusion Detection System), and the Prelude Manager. It
provides a convenient interface for sending and receiving IDMEF (Information
and Event Message Exchange Format) alerts to Prelude Manager with transparent
SSL, fail-over and replication support, asynchronous events and timer
interfaces, an abstracted configuration API (hooking at the command-line, the
configuration line, or wide configuration, available from the Manager), and a
generic plugin API. It allows you to easily turn your favorite security program
into a Prelude sensor.

Installing
----------

Install requirements to build the C part:

.. code-block:: text

    yum group install "Development Tools"

    yum install python-devel

Install and update using `pip`_:

.. code-block:: text

    pip install -U prelude

A Simple Example
----------------

.. code-block:: python

    import prelude

    if __name__ == '__main__':
        idmef = prelude.IDMEF()
        idmef.set("alert.classification.text", "Hello world!")
        print(idmef)


Links
-----

-   Website: https://www.prelude-siem.org/
-   Documentation: https://www.prelude-siem.org/projects/prelude/wiki
-   Releases: https://www.prelude-siem.org/projects/prelude/files
-   Code: https://github.com/Prelude-SIEM/libprelude
-   Issue tracker: https://www.prelude-siem.org/projects/prelude/issues
-   Official chat: irc://#prelude@irc.freenode.net

.. _IDMEF: https://tools.ietf.org/html/rfc4765
.. _pip: https://pip.pypa.io/en/stable/quickstart/
