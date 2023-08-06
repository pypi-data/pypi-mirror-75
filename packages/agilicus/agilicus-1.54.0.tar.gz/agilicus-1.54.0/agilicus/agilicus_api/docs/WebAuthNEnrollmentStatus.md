# WebAuthNEnrollmentStatus

The status of the WebAuthN challenge enrollment.
## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | This member contains the string \&quot;create\&quot; when creating new credentials, and \&quot;get\&quot; when getting an assertion from an existing credential. The purpose of this member is to prevent certain types of signature confusion attacks.  | [optional] 
**challenge** | **str** | An opaque string used to challenge a user attempting to login using WebAuthN. The second factor device will return a signed version of this challenge to indicate that the user should be allowed to proceed.  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


