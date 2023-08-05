from __future__ import unicode_literals
from moto.core.responses import BaseResponse
from moto.core.utils import camelcase_to_underscores
from moto.ec2.utils import filters_from_querystring


class VPCs(BaseResponse):
    def _get_doc_date(self):
        return (
            "2013-10-15"
            if "Boto/" in self.headers.get("user-agent", "")
            else "2016-11-15"
        )

    def create_vpc(self):
        cidr_block = self._get_param("CidrBlock")
        instance_tenancy = self._get_param("InstanceTenancy", if_none="default")
        amazon_provided_ipv6_cidr_blocks = self._get_param(
            "AmazonProvidedIpv6CidrBlock"
        )
        vpc = self.ec2_backend.create_vpc(
            cidr_block,
            instance_tenancy,
            amazon_provided_ipv6_cidr_block=amazon_provided_ipv6_cidr_blocks,
        )
        doc_date = self._get_doc_date()
        template = self.response_template(CREATE_VPC_RESPONSE)
        return template.render(vpc=vpc, doc_date=doc_date)

    def delete_vpc(self):
        vpc_id = self._get_param("VpcId")
        vpc = self.ec2_backend.delete_vpc(vpc_id)
        template = self.response_template(DELETE_VPC_RESPONSE)
        return template.render(vpc=vpc)

    def describe_vpcs(self):
        vpc_ids = self._get_multi_param("VpcId")
        filters = filters_from_querystring(self.querystring)
        vpcs = self.ec2_backend.get_all_vpcs(vpc_ids=vpc_ids, filters=filters)
        doc_date = (
            "2013-10-15"
            if "Boto/" in self.headers.get("user-agent", "")
            else "2016-11-15"
        )
        template = self.response_template(DESCRIBE_VPCS_RESPONSE)
        return template.render(vpcs=vpcs, doc_date=doc_date)

    def describe_vpc_attribute(self):
        vpc_id = self._get_param("VpcId")
        attribute = self._get_param("Attribute")
        attr_name = camelcase_to_underscores(attribute)
        value = self.ec2_backend.describe_vpc_attribute(vpc_id, attr_name)
        template = self.response_template(DESCRIBE_VPC_ATTRIBUTE_RESPONSE)
        return template.render(vpc_id=vpc_id, attribute=attribute, value=value)

    def describe_vpc_classic_link_dns_support(self):
        vpc_ids = self._get_multi_param("VpcIds")
        filters = filters_from_querystring(self.querystring)
        vpcs = self.ec2_backend.get_all_vpcs(vpc_ids=vpc_ids, filters=filters)
        doc_date = self._get_doc_date()
        template = self.response_template(
            DESCRIBE_VPC_CLASSIC_LINK_DNS_SUPPORT_RESPONSE
        )
        return template.render(vpcs=vpcs, doc_date=doc_date)

    def enable_vpc_classic_link_dns_support(self):
        vpc_id = self._get_param("VpcId")
        classic_link_dns_supported = self.ec2_backend.enable_vpc_classic_link_dns_support(
            vpc_id=vpc_id
        )
        doc_date = self._get_doc_date()
        template = self.response_template(ENABLE_VPC_CLASSIC_LINK_DNS_SUPPORT_RESPONSE)
        return template.render(
            classic_link_dns_supported=classic_link_dns_supported, doc_date=doc_date
        )

    def disable_vpc_classic_link_dns_support(self):
        vpc_id = self._get_param("VpcId")
        classic_link_dns_supported = self.ec2_backend.disable_vpc_classic_link_dns_support(
            vpc_id=vpc_id
        )
        doc_date = self._get_doc_date()
        template = self.response_template(DISABLE_VPC_CLASSIC_LINK_DNS_SUPPORT_RESPONSE)
        return template.render(
            classic_link_dns_supported=classic_link_dns_supported, doc_date=doc_date
        )

    def describe_vpc_classic_link(self):
        vpc_ids = self._get_multi_param("VpcId")
        filters = filters_from_querystring(self.querystring)
        vpcs = self.ec2_backend.get_all_vpcs(vpc_ids=vpc_ids, filters=filters)
        doc_date = self._get_doc_date()
        template = self.response_template(DESCRIBE_VPC_CLASSIC_LINK_RESPONSE)
        return template.render(vpcs=vpcs, doc_date=doc_date)

    def enable_vpc_classic_link(self):
        vpc_id = self._get_param("VpcId")
        classic_link_enabled = self.ec2_backend.enable_vpc_classic_link(vpc_id=vpc_id)
        doc_date = self._get_doc_date()
        template = self.response_template(ENABLE_VPC_CLASSIC_LINK_RESPONSE)
        return template.render(
            classic_link_enabled=classic_link_enabled, doc_date=doc_date
        )

    def disable_vpc_classic_link(self):
        vpc_id = self._get_param("VpcId")
        classic_link_enabled = self.ec2_backend.disable_vpc_classic_link(vpc_id=vpc_id)
        doc_date = self._get_doc_date()
        template = self.response_template(DISABLE_VPC_CLASSIC_LINK_RESPONSE)
        return template.render(
            classic_link_enabled=classic_link_enabled, doc_date=doc_date
        )

    def modify_vpc_attribute(self):
        vpc_id = self._get_param("VpcId")

        for attribute in ("EnableDnsSupport", "EnableDnsHostnames"):
            if self.querystring.get("%s.Value" % attribute):
                attr_name = camelcase_to_underscores(attribute)
                attr_value = self.querystring.get("%s.Value" % attribute)[0]
                self.ec2_backend.modify_vpc_attribute(vpc_id, attr_name, attr_value)
                return MODIFY_VPC_ATTRIBUTE_RESPONSE

    def associate_vpc_cidr_block(self):
        vpc_id = self._get_param("VpcId")
        amazon_provided_ipv6_cidr_blocks = self._get_param(
            "AmazonProvidedIpv6CidrBlock"
        )
        # todo test on AWS if can create an association for IPV4 and IPV6 in the same call?
        cidr_block = (
            self._get_param("CidrBlock")
            if not amazon_provided_ipv6_cidr_blocks
            else None
        )
        value = self.ec2_backend.associate_vpc_cidr_block(
            vpc_id, cidr_block, amazon_provided_ipv6_cidr_blocks
        )
        if not amazon_provided_ipv6_cidr_blocks:
            render_template = ASSOCIATE_VPC_CIDR_BLOCK_RESPONSE
        else:
            render_template = IPV6_ASSOCIATE_VPC_CIDR_BLOCK_RESPONSE
        template = self.response_template(render_template)
        return template.render(
            vpc_id=vpc_id,
            value=value,
            cidr_block=value["cidr_block"],
            association_id=value["association_id"],
            cidr_block_state="associating",
        )

    def disassociate_vpc_cidr_block(self):
        association_id = self._get_param("AssociationId")
        value = self.ec2_backend.disassociate_vpc_cidr_block(association_id)
        if "::" in value.get("cidr_block", ""):
            render_template = IPV6_DISASSOCIATE_VPC_CIDR_BLOCK_RESPONSE
        else:
            render_template = DISASSOCIATE_VPC_CIDR_BLOCK_RESPONSE
        template = self.response_template(render_template)
        return template.render(
            vpc_id=value["vpc_id"],
            cidr_block=value["cidr_block"],
            association_id=value["association_id"],
            cidr_block_state="disassociating",
        )

    def create_vpc_endpoint(self):
        vpc_id = self._get_param("VpcId")
        service_name = self._get_param("ServiceName")
        route_table_ids = self._get_multi_param("RouteTableId")
        subnet_ids = self._get_multi_param("SubnetId")
        type = self._get_param("VpcEndpointType")
        policy_document = self._get_param("PolicyDocument")
        client_token = self._get_param("ClientToken")
        tag_specifications = self._get_param("TagSpecifications")
        private_dns_enabled = self._get_param("PrivateDNSEnabled")
        security_group = self._get_param("SecurityGroup")

        vpc_end_point = self.ec2_backend.create_vpc_endpoint(
            vpc_id=vpc_id,
            service_name=service_name,
            type=type,
            policy_document=policy_document,
            route_table_ids=route_table_ids,
            subnet_ids=subnet_ids,
            client_token=client_token,
            security_group=security_group,
            tag_specifications=tag_specifications,
            private_dns_enabled=private_dns_enabled,
        )

        template = self.response_template(CREATE_VPC_END_POINT)
        return template.render(vpc_end_point=vpc_end_point)


CREATE_VPC_RESPONSE = """
<CreateVpcResponse xmlns="http://ec2.amazonaws.com/doc/{{doc_date}}/">
   <requestId>7a62c49f-347e-4fc4-9331-6e8eEXAMPLE</requestId>
   <vpc>
      <vpcId>{{ vpc.id }}</vpcId>
      <state>pending</state>
      <cidrBlock>{{ vpc.cidr_block }}</cidrBlock>
      {% if doc_date == "2016-11-15" %}
          <cidrBlockAssociationSet>
              {% for assoc in vpc.get_cidr_block_association_set() %}
                <item>
                    <cidrBlock>{{assoc.cidr_block}}</cidrBlock>
                    <associationId>{{ assoc.association_id }}</associationId>
                    <cidrBlockState>
                        <state>{{assoc.cidr_block_state.state}}</state>
                    </cidrBlockState>
                </item>
              {% endfor %}
          </cidrBlockAssociationSet>
          <ipv6CidrBlockAssociationSet>
              {% for assoc in vpc.get_cidr_block_association_set(ipv6=True) %}
                <item>
                    <ipv6CidrBlock>{{assoc.cidr_block}}</ipv6CidrBlock>
                    <associationId>{{ assoc.association_id }}</associationId>
                    <ipv6CidrBlockState>
                        <state>{{assoc.cidr_block_state.state}}</state>
                    </ipv6CidrBlockState>
                </item>
              {% endfor %}
          </ipv6CidrBlockAssociationSet>
        {% endif %}
      <dhcpOptionsId>{% if vpc.dhcp_options %}{{ vpc.dhcp_options.id }}{% else %}dopt-1a2b3c4d2{% endif %}</dhcpOptionsId>
      <instanceTenancy>{{ vpc.instance_tenancy }}</instanceTenancy>
      <tagSet>
        {% for tag in vpc.get_tags() %}
          <item>
            <resourceId>{{ tag.resource_id }}</resourceId>
            <resourceType>{{ tag.resource_type }}</resourceType>
            <key>{{ tag.key }}</key>
            <value>{{ tag.value }}</value>
          </item>
        {% endfor %}
      </tagSet>
   </vpc>
</CreateVpcResponse>"""

DESCRIBE_VPC_CLASSIC_LINK_DNS_SUPPORT_RESPONSE = """
<DescribeVpcClassicLinkDnsSupportResponse xmlns="http://ec2.amazonaws.com/doc/{{doc_date}}/">
  <requestId>7a62c442-3484-4f42-9342-6942EXAMPLE</requestId>
  <vpcs>
    {% for vpc in vpcs %}
      <item>
        <vpcId>{{ vpc.id }}</vpcId>
        <classicLinkDnsSupported>{{ vpc.classic_link_dns_supported }}</classicLinkDnsSupported>
      </item>
    {% endfor %}
  </vpcs>
</DescribeVpcClassicLinkDnsSupportResponse>"""

ENABLE_VPC_CLASSIC_LINK_DNS_SUPPORT_RESPONSE = """
<EnableVpcClassicLinkDnsSupportResponse xmlns="http://ec2.amazonaws.com/doc/{{doc_date}}/">
  <requestId>7a62c442-3484-4f42-9342-6942EXAMPLE</requestId>
  <return>{{ classic_link_dns_supported }}</return>
</EnableVpcClassicLinkDnsSupportResponse>"""

DISABLE_VPC_CLASSIC_LINK_DNS_SUPPORT_RESPONSE = """
<DisableVpcClassicLinkDnsSupportResponse xmlns="http://ec2.amazonaws.com/doc/{{doc_date}}/">
  <requestId>7a62c442-3484-4f42-9342-6942EXAMPLE</requestId>
  <return>{{ classic_link_dns_supported }}</return>
</DisableVpcClassicLinkDnsSupportResponse>"""

DESCRIBE_VPC_CLASSIC_LINK_RESPONSE = """
<DescribeVpcClassicLinkResponse xmlns="http://ec2.amazonaws.com/doc/{{doc_date}}/">
  <requestId>7a62c442-3484-4f42-9342-6942EXAMPLE</requestId>
  <vpcSet>
    {% for vpc in vpcs %}
      <item>
        <vpcId>{{ vpc.id }}</vpcId>
        <classicLinkEnabled>{{ vpc.classic_link_enabled }}</classicLinkEnabled>
      </item>
    {% endfor %}
  </vpcSet>
</DescribeVpcClassicLinkResponse>"""

ENABLE_VPC_CLASSIC_LINK_RESPONSE = """
<EnableVpcClassicLinkResponse xmlns="http://ec2.amazonaws.com/doc/{{doc_date}}/">
  <requestId>7a62c442-3484-4f42-9342-6942EXAMPLE</requestId>
  <return>{{ classic_link_enabled }}</return>
</EnableVpcClassicLinkResponse>"""

DISABLE_VPC_CLASSIC_LINK_RESPONSE = """
<DisableVpcClassicLinkResponse xmlns="http://ec2.amazonaws.com/doc/{{doc_date}}/">
  <requestId>7a62c442-3484-4f42-9342-6942EXAMPLE</requestId>
  <return>{{ classic_link_enabled }}</return>
</DisableVpcClassicLinkResponse>"""

DESCRIBE_VPCS_RESPONSE = """
<DescribeVpcsResponse xmlns="http://ec2.amazonaws.com/doc/{{doc_date}}/">
  <requestId>7a62c442-3484-4f42-9342-6942EXAMPLE</requestId>
  <vpcSet>
    {% for vpc in vpcs %}
      <item>
        <vpcId>{{ vpc.id }}</vpcId>
        <state>{{ vpc.state }}</state>
        <cidrBlock>{{ vpc.cidr_block }}</cidrBlock>
        {% if doc_date == "2016-11-15" %}
            <cidrBlockAssociationSet>
              {% for assoc in vpc.get_cidr_block_association_set() %}
                <item>
                    <cidrBlock>{{assoc.cidr_block}}</cidrBlock>
                    <associationId>{{ assoc.association_id }}</associationId>
                    <cidrBlockState>
                        <state>{{assoc.cidr_block_state.state}}</state>
                    </cidrBlockState>
                </item>
              {% endfor %}
            </cidrBlockAssociationSet>
            <ipv6CidrBlockAssociationSet>
              {% for assoc in vpc.get_cidr_block_association_set(ipv6=True) %}
                <item>
                    <ipv6CidrBlock>{{assoc.cidr_block}}</ipv6CidrBlock>
                    <associationId>{{ assoc.association_id }}</associationId>
                    <ipv6CidrBlockState>
                        <state>{{assoc.cidr_block_state.state}}</state>
                    </ipv6CidrBlockState>
                </item>
              {% endfor %}
            </ipv6CidrBlockAssociationSet>
        {% endif %}
        <dhcpOptionsId>{% if vpc.dhcp_options %}{{ vpc.dhcp_options.id }}{% else %}dopt-7a8b9c2d{% endif %}</dhcpOptionsId>
        <instanceTenancy>{{ vpc.instance_tenancy }}</instanceTenancy>
        <isDefault>{{ vpc.is_default }}</isDefault>
        <tagSet>
          {% for tag in vpc.get_tags() %}
            <item>
              <resourceId>{{ tag.resource_id }}</resourceId>
              <resourceType>{{ tag.resource_type }}</resourceType>
              <key>{{ tag.key }}</key>
              <value>{{ tag.value }}</value>
            </item>
          {% endfor %}
        </tagSet>
      </item>
    {% endfor %}
  </vpcSet>
</DescribeVpcsResponse>"""

DELETE_VPC_RESPONSE = """
<DeleteVpcResponse xmlns="http://ec2.amazonaws.com/doc/2016-11-15/">
   <requestId>7a62c49f-347e-4fc4-9331-6e8eEXAMPLE</requestId>
   <return>true</return>
</DeleteVpcResponse>
"""

DESCRIBE_VPC_ATTRIBUTE_RESPONSE = """
<DescribeVpcAttributeResponse xmlns="http://ec2.amazonaws.com/doc/2016-11-15/">
  <requestId>7a62c49f-347e-4fc4-9331-6e8eEXAMPLE</requestId>
  <vpcId>{{ vpc_id }}</vpcId>
  <{{ attribute }}>
    <value>{{ value }}</value>
  </{{ attribute }}>
</DescribeVpcAttributeResponse>"""

MODIFY_VPC_ATTRIBUTE_RESPONSE = """
<ModifyVpcAttributeResponse xmlns="http://ec2.amazonaws.com/doc/2016-11-15/">
  <requestId>7a62c49f-347e-4fc4-9331-6e8eEXAMPLE</requestId>
  <return>true</return>
</ModifyVpcAttributeResponse>"""

ASSOCIATE_VPC_CIDR_BLOCK_RESPONSE = """
<AssociateVpcCidrBlockResponse xmlns="http://ec2.amazonaws.com/doc/2016-11-15/">
    <requestId>7a62c49f-347e-4fc4-9331-6e8eEXAMPLE</requestId>
    <vpcId>{{vpc_id}}</vpcId>
    <cidrBlockAssociation>
        <associationId>{{association_id}}</associationId>
        <cidrBlock>{{cidr_block}}</cidrBlock>
        <cidrBlockState>
            <state>{{cidr_block_state}}</state>
        </cidrBlockState>
    </cidrBlockAssociation>
</AssociateVpcCidrBlockResponse>"""

DISASSOCIATE_VPC_CIDR_BLOCK_RESPONSE = """
<DisassociateVpcCidrBlockResponse xmlns="http://ec2.amazonaws.com/doc/2016-11-15/">
    <requestId>7a62c49f-347e-4fc4-9331-6e8eEXAMPLE</requestId>
    <vpcId>{{vpc_id}}</vpcId>
    <cidrBlockAssociation>
        <associationId>{{association_id}}</associationId>
        <cidrBlock>{{cidr_block}}</cidrBlock>
        <cidrBlockState>
            <state>{{cidr_block_state}}</state>
        </cidrBlockState>
    </cidrBlockAssociation>
</DisassociateVpcCidrBlockResponse>"""

IPV6_ASSOCIATE_VPC_CIDR_BLOCK_RESPONSE = """
<AssociateVpcCidrBlockResponse xmlns="http://ec2.amazonaws.com/doc/2016-11-15/">
    <requestId>33af6c54-1139-4d50-b4f7-15a8example</requestId>
    <vpcId>{{vpc_id}}</vpcId>
    <ipv6CidrBlockAssociation>
        <associationId>{{association_id}}</associationId>
        <ipv6CidrBlock>{{cidr_block}}</ipv6CidrBlock>
        <ipv6CidrBlockState>
            <state>{{cidr_block_state}}</state>
        </ipv6CidrBlockState>
    </ipv6CidrBlockAssociation>
</AssociateVpcCidrBlockResponse>"""

IPV6_DISASSOCIATE_VPC_CIDR_BLOCK_RESPONSE = """
<DisassociateVpcCidrBlockResponse xmlns="http://ec2.amazonaws.com/doc/2016-11-15/">
    <requestId>33af6c54-1139-4d50-b4f7-15a8example</requestId>
    <vpcId>{{vpc_id}}</vpcId>
    <ipv6CidrBlockAssociation>
        <associationId>{{association_id}}</associationId>
        <ipv6CidrBlock>{{cidr_block}}</ipv6CidrBlock>
        <ipv6CidrBlockState>
            <state>{{cidr_block_state}}</state>
        </ipv6CidrBlockState>
    </ipv6CidrBlockAssociation>
</DisassociateVpcCidrBlockResponse>"""

CREATE_VPC_END_POINT = """ <CreateVpcEndpointResponse xmlns="http://monitoring.amazonaws.com/doc/2010-08-01/">
    <vpcEndpoint>
        <policyDocument>{{ vpc_end_point.policy_document }}</policyDocument>
        <state> available </state>
        <vpcEndpointPolicySupported> false </vpcEndpointPolicySupported>
        <serviceName>{{ vpc_end_point.service_name }}</serviceName>
        <vpcId>{{ vpc_end_point.vpc_id }}</vpcId>
        <vpcEndpointId>{{ vpc_end_point.id }}</vpcEndpointId>
        <routeTableIdSet>
            {% for routeid in vpc_end_point.route_table_ids %}
                <item>{{ routeid }}</item>
            {% endfor %}
        </routeTableIdSet>
        <networkInterfaceIdSet>
            {% for network_interface_id in vpc_end_point.network_interface_ids %}
                <item>{{ network_interface_id }}</item>
            {% endfor %}
        </networkInterfaceIdSet>
        <subnetIdSet>
            {% for subnetId in vpc_end_point.subnet_ids %}
                <item>{{ subnetId }}</item>
            {% endfor %}
        </subnetIdSet>
        <dnsEntrySet>
        {% if vpc_end_point.dns_entries  %}
            {% for entry in vpc_end_point.dns_entries %}
            <item>
                <hostedZoneId>{{ entry["hosted_zone_id"] }}</hostedZoneId>
                <dnsName>{{ entry["dns_name"] }}</dnsName>
            </item>
            {% endfor %}
        {% endif %}
        </dnsEntrySet>
        <creationTimestamp>{{ vpc_end_point.created_at }}</creationTimestamp>
    </vpcEndpoint>
</CreateVpcEndpointResponse>"""
