# OIDCUpstreamIdentityProvider

Custom OIDC Upstream Identity Provider
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | A name used to uniquely refer to the upstream identity provider configuration. This is the text that will be displayed when presenting the upstream identity for login. | 
**issuer** | **str** | The upstream issuer uri. This is the URI which identifies the issuer against which users selecting this OIDCUpstreamIdentityProvider will authenticate. The issuer must support the OpenID Connect discovery document described here: https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderConfig. | 
**client_id** | **str** | The client ID for the upstream identity provider | 
**client_secret** | **str** | The secret presented to the upstream during any workflows which require authentication | [optional] 
**issuer_external_host** | **str** | A proxy standing in for the main issuer host. Use this if fronting the upstream through the Agilicus infrastructure | [optional] 
**username_key** | **str** | Allows changing the key in the OIDC response claims used to determine the full name of the user. If not present, defaults to the standard name | [optional] 
**email_key** | **str** | Allows changing the key in the OIDC response claims used to determine the email address of the user. If not present, defaults to the standard email | [optional] 
**email_verification_required** | **bool** | Controls whether email verification is required for this OIDC provider. Some OIDC providers do not take steps to verify the email address of users, or may not do so in all cases. Setting this value to true will reject any successful upstream logins for users which have not had their email address verified. | [optional] [default to True]
**request_user_info** | **bool** | Controls whether the system will retrieve extra information about the user from the provider&#39;s user_info endpoint. This can be useful if the initial OIDC response does not contain sufficient information to determine the email address or user&#39;s name. Setting this value to true will cause extra requests to be generated to the upstream every time a user logs in to it. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


