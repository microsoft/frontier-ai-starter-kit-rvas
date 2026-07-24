@description('Name used to identify this customer-owned approved-content pack.')
param contentPackName string = 'avatar-onboarding-demo'

@description('Selected platform identifier or adapter name. This deployment creates no platform resources.')
param deliveryAdapterName string = 'mock-adapter'

@description('Optional non-secret endpoint or configuration reference owned by the customer.')
param deliveryConfigurationReference string = ''

@description('URI or repository reference for the approved-content pack; do not place sensitive data here.')
param approvedContentReference string = ''

output integrationSeam object = {
  contentPackName: contentPackName
  deliveryAdapterName: deliveryAdapterName
  deliveryConfigurationReference: deliveryConfigurationReference
  approvedContentReference: approvedContentReference
  requiresHumanApproval: true
  requiredExperienceControls: [
    'avatar-disclosure'
    'captions-and-transcript'
    'language-and-non-avatar-fallback'
    'feedback-and-operational-evidence'
    'withdrawal-control'
  ]
}
