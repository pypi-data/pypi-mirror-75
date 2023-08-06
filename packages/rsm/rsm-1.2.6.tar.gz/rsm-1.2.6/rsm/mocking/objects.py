class Entity:
    """
        This class represents an entity object.
    """

    def __init__(self):

        self.additional_properties = None

        self.modification_time = None
        self.alert_identifier = None
        self.case_identifier = None

        self.creation_time = None
        self.is_suspicious = None
        self.is_vulnerable = None

        self.entity_type = None
        self.is_internal = None
        self.is_artifact = None
        self.is_enriched = None
        self.identifier = None

        self.is_pivot = None

    @property
    def to_dict(self) -> dict:
        return self.__dict__

    def _update_internal_properties(self):
        self.additional_properties["IsEnriched"] = str(self.is_enriched)
        self.additional_properties["IsSuspicious"] = str(self.is_suspicious)
        self.additional_properties["IsVulnerable"] = str(self.is_vulnerable)
        self.additional_properties["IsInternalAsset"] = str(self.is_internal)

    def __repr__(self):
        """
        Printable representation of the object, useful for developers
        """
        return self.identifier

    def __str__(self):
        """
        Printable representation of the object, end users
        """
        return self.identifier


class Event:
    def __init__(self):
        self.modification_time = None
        self.creation_time = None
        self.identifier = None

        self.alert_identifier = None

        self.description = None
        self.event_id = None
        self.name = None

        self.device_severity = None
        self.device_product = None
        self.device_version = None
        self.event_class_id = None
        self.device_vendor = None

        self.is_correlation = None
        self.rule_generator = None
        self.event_type = None
        self.start_time = None
        self.severity = None
        self.end_time = None

        self.source_dns_domain = None
        self.device_host_name = None
        self.source_host_name = None
        self.device_address = None
        self.source_address = None

        self.source_user_name = None
        self.source_user_id = None

        self.destination_process_name = None
        self.destination_mac_address = None
        self.destination_dns_domain = None
        self.destination_nt_domain = None
        self.destination_host_name = None
        self.destination_user_name = None
        self.destination_address = None
        self.source_process_name = None
        self.source_mac_address = None
        self.destination_port = None
        self.destination_url = None

        self.file_name = None
        self.file_hash = None
        self.file_type = None

        self.application_protocol = None
        self.transport_protocol = None
        self.category_outcome = None
        self.email_subject = None

        self.additional_properties = None
        self.threat_campaign = None
        self.generic_entity = None
        self.threat_actor = None
        self.phone_number = None
        self.credit_card = None
        self.deployment = None
        self.signature = None
        self.cve = None
        self.usb = None


class AlertInfo:
    def __init__(self):

        self.alert_group_identifier = None
        self.additional_properties = None
        self.modification_time = None
        self.reporting_product = None
        self.reporting_vendor = None
        self.case_identifier = None
        self.additional_data = None
        self.rule_generator = None
        self.creation_time = None
        self.detected_time = None
        self.external_id = None
        self.description = None
        self.environment = None
        self.identifier = None
        self.severity = None
        self.name = None
        self.tags = None


class Case:
    """
        This class represents a Case object
    """

    def __init__(self):

        self.additional_properties = None
        self.modification_time = None
        self.creation_time = None
        self.identifier = None

        self.assigned_user = None
        self.is_important = None
        self.environment = None
        self.is_touched = None
        self.is_merged = None

        self.description = None
        self.priority = None
        self.status = None
        self.stage = None
        self.title = None

        self.sla_expiration_unix_time = None
        self.has_suspicious_entity = None
        self.high_risk_products = None
        self.has_workflow = None
        self.is_incident = None
        self.alert_count = None
        self.start_time = None
        self.is_locked = None


class CaseInfo:
    def __init__(self):
        self.environment = None
        self.description = None
        self.display_id = None
        self.ticket_id = None
        self.reason = None
        self.name = None
        self.device_product = None
        self.device_vendor = None
        self.start_time = None
        self.end_time = None

        self.is_test_case = False
        self.priority = -1

        self.source_grouping_identifier = None
        self.rule_generator = None
        self.attachments = []
        self.extensions = {}
        self.events = []

obj = CaseInfo()
