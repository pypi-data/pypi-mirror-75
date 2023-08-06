QUERY = {
    'AddEmailProvider': '''
mutation AddEmailProvider($options: EmailProviderListInput) {
  AddEmailProvider(options: $options) {
    _id
    name
    image
    description
    fields {
      label
      type
      placeholder
      help
      value
      options
    }
    client
    user
    status
    provider {
      _id
      name
      image
      description
      client
      user
      status
    }
  }
}''',
    'AddLDAPServer': '''
mutation AddLDAPServer($name: String!, $clientId: String!, $userId: String!, $ldapLink: String!, $baseDN: String!, $searchStandard: String!, $username: String!, $password: String!, $emailPostfix: String, $description: String, $enabled: Boolean){
    AddLDAPServer(name: $name, clientId: $clientId, userId: $userId, ldapLink: $ldapLink, baseDN: $baseDN, searchStandard: $searchStandard, username: $username, password: $password, emailPostfix: $emailPostfix, description: $description, enabled: $enabled){
        _id
        name
        clientId
        userId
        ldapLink
        baseDN
        searchStandard
        emailPostfix
        username
        password
        description
        enabled
        isDeleted
        createdAt
        updatedAt
    }
}
''',
    'AddOAuthList': '''
mutation AddOAuthList($options: OAuthListUpdateInput, $fields: [OAuthListFieldsFormUpdateInput]){
    AddOAuthList(options: $options, fields: $fields){
        _id
        name
        alias
        image
        description
        enabled
        url
        client
        user
        oAuthUrl
        wxappLogo
        fields{
            label
            type
            placeholder
            value
            checked
        }
        oauth{
            _id
            name
            alias
            image
            description
            enabled
            url
            client
            user
            oAuthUrl
            wxappLogo
        }
    }
}
''',
    'AddSystemPricing': '''
mutation AddSystemPricing($options: PricingFieldsInput){
    AddSystemPricing(options: $options){
        _id
        type
        startNumber
        freeNumber
        startPrice
        maxNumber
        d
        features
    }
}
''',
    'ClearAvatarSrc': '''
mutation ClearAvatarSrc($client: String, $oauth: String, $user: String){
    ClearAvatarSrc(client: $client, oauth: $oauth, user: $user){
        _id
        name
        alias
        image
        description
        enabled
        url
        client
        user
        oAuthUrl
        wxappLogo
        fields{
            label
            type
            placeholder
            value
            checked
        }
        oauth{
            _id
            name
            alias
            image
            description
            enabled
            url
            client
            user
            oAuthUrl
            wxappLogo
        }
    }
}
''',
    'ContinuePay': '''
mutation ContinuePay($order: String!){
    ContinuePay(order: $order){
        code
        url
        charge
    }
}
''',
    'CreateDefaultSAMLIdentityProviderSettings': '''
mutation CreateDefaultSAMLIdentityProviderSettings($name: String!, $image: String, $description: String, $mappings: AssertionMapInputType){
    CreateDefaultSAMLIdentityProviderSettings(name: $name, image: $image, description: $description, mappings: $mappings){
        _id
        name
        image
        description
        mappings{
            username
            nickname
            photo
            company
            providerName
            email
        }
        isDeleted
    }
}
''',
    'CreateOAuthProvider': '''
mutation CreateOAuthProvider($name: String!, $domain: String!, $redirectUris: [String]!, $grants: [String!]!, $clientId: String, $image: String, $description: String, $homepageURL: String, $casExpire: Int){
    CreateOAuthProvider(name: $name, domain: $domain, redirectUris: $redirectUris, grants: $grants, clientId: $clientId, image: $image, description: $description, homepageURL: $homepageURL, casExpire: $casExpire){
        _id
        name
        domain
        image
        redirectUris
        appSecret
        client_id
        clientId
        grants
        description
        homepageURL
        isDeleted
        when
        css
        loginUrl
        casExpire
    }
}
''',
    'CreateOIDCApp': '''
mutation CreateOIDCApp($name: String!, $domain: String!, $redirect_uris: [String]!, $grant_types: [String!]!, $response_types: [String!]!, $clientId: String, $client_id: String, $token_endpoint_auth_method: String, $image: String, $isDefault: Boolean, $id_token_signed_response_alg: String, $id_token_encrypted_response_alg: String, $id_token_encrypted_response_enc: String, $userinfo_signed_response_alg: String, $userinfo_encrypted_response_alg: String, $userinfo_encrypted_response_enc: String, $request_object_signing_alg: String, $request_object_encryption_alg: String, $request_object_encryption_enc: String, $jwks_uri: String, $_jwks_uri: String, $jwks: String, $_jwks: String, $custom_jwks: String, $description: String, $homepageURL: String, $authorization_code_expire: String, $id_token_expire: String, $access_token_expire: String, $cas_expire: String, $customStyles: OIDCProviderCustomStylesInput){
    CreateOIDCApp(name: $name, domain: $domain, redirect_uris: $redirect_uris, grant_types: $grant_types, response_types: $response_types, clientId: $clientId, client_id: $client_id, token_endpoint_auth_method: $token_endpoint_auth_method, image: $image, isDefault: $isDefault, id_token_signed_response_alg: $id_token_signed_response_alg, id_token_encrypted_response_alg: $id_token_encrypted_response_alg, id_token_encrypted_response_enc: $id_token_encrypted_response_enc, userinfo_signed_response_alg: $userinfo_signed_response_alg, userinfo_encrypted_response_alg: $userinfo_encrypted_response_alg, userinfo_encrypted_response_enc: $userinfo_encrypted_response_enc, request_object_signing_alg: $request_object_signing_alg, request_object_encryption_alg: $request_object_encryption_alg, request_object_encryption_enc: $request_object_encryption_enc, jwks_uri: $jwks_uri, _jwks_uri: $_jwks_uri, jwks: $jwks, _jwks: $_jwks, custom_jwks: $custom_jwks, description: $description, homepageURL: $homepageURL, authorization_code_expire: $authorization_code_expire, id_token_expire: $id_token_expire, access_token_expire: $access_token_expire, cas_expire: $cas_expire, customStyles: $customStyles){
        _id
        name
        domain
        image
        redirect_uris
        client_id
        client_secret
        token_endpoint_auth_method
        id_token_signed_response_alg
        id_token_encrypted_response_alg
        id_token_encrypted_response_enc
        userinfo_signed_response_alg
        userinfo_encrypted_response_alg
        userinfo_encrypted_response_enc
        request_object_signing_alg
        request_object_encryption_alg
        request_object_encryption_enc
        jwks_uri
        _jwks_uri
        custom_jwks
        jwks
        _jwks
        clientId
        grant_types
        response_types
        description
        homepageURL
        isDeleted
        isDefault
        when
        css
        authorization_code_expire
        id_token_expire
        access_token_expire
        cas_expire
        loginUrl
        customStyles{
            forceLogin
            hideQRCode
            hideUP
            hideUsername
            hideRegister
            hidePhone
            hideSocial
            hideClose
            hidePhonePassword
            defaultLoginMethod
        }
    }
}
''',
    'CreateSAMLIdentityProvider': '''
mutation CreateSAMLIdentityProvider($name: String!, $domain: String!, $clientId: String!, $image: String, $description: String, $SPMetadata: String, $IdPMetadata: String){
    CreateSAMLIdentityProvider(name: $name, domain: $domain, clientId: $clientId, image: $image, description: $description, SPMetadata: $SPMetadata, IdPMetadata: $IdPMetadata){
        _id
        name
        domain
        image
        appSecret
        appId
        clientId
        description
        isDeleted
        enabled
        when
        SPMetadata
        attributeNameFormat
        customAttributes
        emailDomainTransformation
        authnContextClassRef
        IdPMetadata
        assertionConsumerUrl
        bindings
        nameIds
        attributes
        enableSignRes
        resSignAlgorithm
        resAbstractAlgorithm
        resSignPublicKey
        resSignPrivateKey
        resSignPrivateKeyPass
        enableSignReq
        reqSignPublicKey
        enableEncryptRes
        resEncryptPublicKey
        css
    }
}
''',
    'CreateSAMLServiceProvider': '''
mutation CreateSAMLServiceProvider($name: String!, $domain: String!, $clientId: String!, $redirectUrl: String!, $description: String, $SPMetadata: String, $IdPMetadata: String, $image: String, $mappings: AssertionMapInputType, $defaultIdPMapId: String){
    CreateSAMLServiceProvider(name: $name, domain: $domain, clientId: $clientId, redirectUrl: $redirectUrl, description: $description, SPMetadata: $SPMetadata, IdPMetadata: $IdPMetadata, image: $image, mappings: $mappings, defaultIdPMapId: $defaultIdPMapId){
        _id
        name
        domain
        image
        appSecret
        defaultIdPMap{
            _id
            name
            image
            description
            isDeleted
        }
        defaultIdPMapId
        appId
        clientId
        description
        isDeleted
        enabled
        when
        SPMetadata
        IdPMetadata
        IdPEntityID
        assertionConsumeService{
            binding
            url
            isDefault
        }
        mappings{
            username
            nickname
            photo
            company
            providerName
            email
        }
        redirectUrl
        loginUrl
        logoutUrl
        nameId
        enableSignRes
        resSignPublicKey
        hasResEncrypted
        resEncryptAlgorithm
        resAbstractAlgorithm
        resDecryptPrivateKey
        resDecryptPrivateKeyPass
        resEncryptPublicKey
        enableSignReq
        reqSignAlgorithm
        reqAbstractAlgorithm
        reqSignPrivateKey
        reqSignPrivateKeyPass
        reqSignPublicKey
        SPUrl
    }
}
''',
    'EnableSAMLIdentityProvider': '''
mutation EnableSAMLIdentityProvider($appId: String!, $clientId: String!, $enabled: Boolean){
    EnableSAMLIdentityProvider(appId: $appId, clientId: $clientId, enabled: $enabled){
        _id
        name
        domain
        image
        appSecret
        appId
        clientId
        description
        isDeleted
        enabled
        when
        SPMetadata
        attributeNameFormat
        customAttributes
        emailDomainTransformation
        authnContextClassRef
        IdPMetadata
        assertionConsumerUrl
        bindings
        nameIds
        attributes
        enableSignRes
        resSignAlgorithm
        resAbstractAlgorithm
        resSignPublicKey
        resSignPrivateKey
        resSignPrivateKeyPass
        enableSignReq
        reqSignPublicKey
        enableEncryptRes
        resEncryptPublicKey
        css
    }
}
''',
    'EnableSAMLServiceProvider': '''
mutation EnableSAMLServiceProvider($appId: String!, $clientId: String!, $enabled: Boolean){
    EnableSAMLServiceProvider(appId: $appId, clientId: $clientId, enabled: $enabled){
        _id
        name
        domain
        image
        appSecret
        defaultIdPMap{
            _id
            name
            image
            description
            isDeleted
        }
        defaultIdPMapId
        appId
        clientId
        description
        isDeleted
        enabled
        when
        SPMetadata
        IdPMetadata
        IdPEntityID
        assertionConsumeService{
            binding
            url
            isDefault
        }
        mappings{
            username
            nickname
            photo
            company
            providerName
            email
        }
        redirectUrl
        loginUrl
        logoutUrl
        nameId
        enableSignRes
        resSignPublicKey
        hasResEncrypted
        resEncryptAlgorithm
        resAbstractAlgorithm
        resDecryptPrivateKey
        resDecryptPrivateKeyPass
        resEncryptPublicKey
        enableSignReq
        reqSignAlgorithm
        reqAbstractAlgorithm
        reqSignPrivateKey
        reqSignPrivateKeyPass
        reqSignPublicKey
        SPUrl
    }
}
''',
    'IncClientFlowNumber': '''
mutation IncClientFlowNumber($user: String, $userInvitied: String, $client: String, $number: Int){
    IncClientFlowNumber(user: $user, userInvitied: $userInvitied, client: $client, number: $number){
        code
        url
        charge
    }
}
''',
    'LoginByLDAP': '''
mutation LoginByLDAP($username: String!, $password: String!, $clientId: String!, $browser: String){
    LoginByLDAP(username: $username, password: $password, clientId: $clientId, browser: $browser){
        _id
        username
        email
        unionid
        openid
        emailVerified
        phone
        phoneVerified
        nickname
        company
        photo
        browser
        password
        registerInClient
        registerMethod
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        device
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        country
        updatedAt
        thirdPartyIdentity{
            provider
            refreshToken
            accessToken
            expiresIn
            updatedAt
        }
        oldPassword
        metadata
    }
}
''',
    'RemoveEmailProvider': '''
mutation RemoveEmailProvider($_ids: [String]!){
    RemoveEmailProvider(_ids: $_ids){
        _id
        name
        image
        description
        fields{
            label
            type
            placeholder
            help
            value
            options
        }
        client
        user
        status
        provider{
            _id
            name
            image
            description
            client
            user
            status
        }
    }
}
''',
    'RemoveLDAPServer': '''
mutation RemoveLDAPServer($ldapId: String!, $clientId: String!){
    RemoveLDAPServer(ldapId: $ldapId, clientId: $clientId){
        _id
        name
        clientId
        userId
        ldapLink
        baseDN
        searchStandard
        emailPostfix
        username
        password
        description
        enabled
        isDeleted
        createdAt
        updatedAt
    }
}
''',
    'RemoveOAuthList': '''
mutation RemoveOAuthList($ids: [String]){
    RemoveOAuthList(ids: $ids)
}
''',
    'RemoveOAuthProvider': '''
mutation RemoveOAuthProvider($appId: String!, $clientId: String!){
    RemoveOAuthProvider(appId: $appId, clientId: $clientId){
        _id
        name
        domain
        image
        redirectUris
        appSecret
        client_id
        clientId
        grants
        description
        homepageURL
        isDeleted
        when
        css
        loginUrl
        casExpire
    }
}
''',
    'RemoveOIDCApp': '''
mutation RemoveOIDCApp($appId: String!, $clientId: String!){
    RemoveOIDCApp(appId: $appId, clientId: $clientId){
        _id
        name
        domain
        image
        redirect_uris
        client_id
        client_secret
        token_endpoint_auth_method
        id_token_signed_response_alg
        id_token_encrypted_response_alg
        id_token_encrypted_response_enc
        userinfo_signed_response_alg
        userinfo_encrypted_response_alg
        userinfo_encrypted_response_enc
        request_object_signing_alg
        request_object_encryption_alg
        request_object_encryption_enc
        jwks_uri
        _jwks_uri
        custom_jwks
        jwks
        _jwks
        clientId
        grant_types
        response_types
        description
        homepageURL
        isDeleted
        isDefault
        when
        css
        authorization_code_expire
        id_token_expire
        access_token_expire
        cas_expire
        loginUrl
        customStyles{
            forceLogin
            hideQRCode
            hideUP
            hideUsername
            hideRegister
            hidePhone
            hideSocial
            hideClose
            hidePhonePassword
            defaultLoginMethod
        }
    }
}
''',
    'RemoveSAMLIdentityProvider': '''
mutation RemoveSAMLIdentityProvider($appId: String!, $clientId: String!){
    RemoveSAMLIdentityProvider(appId: $appId, clientId: $clientId){
        _id
        name
        domain
        image
        appSecret
        appId
        clientId
        description
        isDeleted
        enabled
        when
        SPMetadata
        attributeNameFormat
        customAttributes
        emailDomainTransformation
        authnContextClassRef
        IdPMetadata
        assertionConsumerUrl
        bindings
        nameIds
        attributes
        enableSignRes
        resSignAlgorithm
        resAbstractAlgorithm
        resSignPublicKey
        resSignPrivateKey
        resSignPrivateKeyPass
        enableSignReq
        reqSignPublicKey
        enableEncryptRes
        resEncryptPublicKey
        css
    }
}
''',
    'RemoveSAMLServiceProvider': '''
mutation RemoveSAMLServiceProvider($appId: String!, $clientId: String!){
    RemoveSAMLServiceProvider(appId: $appId, clientId: $clientId){
        _id
        name
        domain
        image
        appSecret
        defaultIdPMap{
            _id
            name
            image
            description
            isDeleted
        }
        defaultIdPMapId
        appId
        clientId
        description
        isDeleted
        enabled
        when
        SPMetadata
        IdPMetadata
        IdPEntityID
        assertionConsumeService{
            binding
            url
            isDefault
        }
        mappings{
            username
            nickname
            photo
            company
            providerName
            email
        }
        redirectUrl
        loginUrl
        logoutUrl
        nameId
        enableSignRes
        resSignPublicKey
        hasResEncrypted
        resEncryptAlgorithm
        resAbstractAlgorithm
        resDecryptPrivateKey
        resDecryptPrivateKeyPass
        resEncryptPublicKey
        enableSignReq
        reqSignAlgorithm
        reqAbstractAlgorithm
        reqSignPrivateKey
        reqSignPrivateKeyPass
        reqSignPublicKey
        SPUrl
    }
}
''',
    'RevokeUserAuthorizedApp': '''
mutation RevokeUserAuthorizedApp($appId: String, $userPoolId: String, $userId: String){
    RevokeUserAuthorizedApp(appId: $appId, userPoolId: $userPoolId, userId: $userId){
        _id
        appId
        userId
        scope
        type
        isRevoked
        when
    }
}
''',
    'SaveEmailProviderWithClient': '''
mutation SaveEmailProviderWithClient($options: EmailProviderWithClientAddInput){
    SaveEmailProviderWithClient(options: $options){
        _id
        user
        client
        status
        fields{
            label
            type
            placeholder
            help
            value
            options
        }
        provider{
            _id
            name
            image
            description
        }
    }
}
''',
    'SendEmail': '''
mutation SendEmail($receivers: [String]!, $subject: String!, $client: String!, $user: String, $testAvailable: Boolean, $providerName: String, $content: String, $sender: String, $meta_data: String, $secret: String){
    SendEmail(receivers: $receivers, subject: $subject, client: $client, user: $user, testAvailable: $testAvailable, providerName: $providerName, content: $content, sender: $sender, meta_data: $meta_data, secret: $secret){
        _id
        user
        subject
        content
        sender
        receivers
        post
        createdAt
        rejected
        isDeleted
        client
    }
}
''',
    'SendEmailByType': '''
mutation SendEmailByType($user: String!, $type: String!, $client: String!, $receivers: [String]!, $meta_data: String){
    SendEmailByType(user: $user, type: $type, client: $client, receivers: $receivers, meta_data: $meta_data){
        _id
        user
        subject
        content
        sender
        receivers
        post
        createdAt
        rejected
        isDeleted
        client
    }
}
''',
    'SendWebhookTest': '''
mutation SendWebhookTest($id: String!){
    SendWebhookTest(id: $id)
}
''',
    'SetApplicationOAuthEnableOrDisable': '''
mutation SetApplicationOAuthEnableOrDisable($client: String, $oauth: String, $user: String, $enabled: Boolean){
    SetApplicationOAuthEnableOrDisable(client: $client, oauth: $oauth, user: $user, enabled: $enabled){
        _id
        name
        alias
        image
        description
        enabled
        url
        client
        user
        oAuthUrl
        wxappLogo
        fields{
            label
            type
            placeholder
            value
            checked
        }
        oauth{
            _id
            name
            alias
            image
            description
            enabled
            url
            client
            user
            oAuthUrl
            wxappLogo
        }
    }
}
''',
    'UpdateApplicationOAuth': '''
mutation UpdateApplicationOAuth($client: String, $oauth: String, $user: String, $alias: String, $fields: [OAuthListFieldsFormUpdateInput]){
    UpdateApplicationOAuth(client: $client, oauth: $oauth, user: $user, alias: $alias, fields: $fields){
        _id
        name
        alias
        image
        description
        enabled
        url
        client
        user
        oAuthUrl
        wxappLogo
        fields{
            label
            type
            placeholder
            value
            checked
        }
        oauth{
            _id
            name
            alias
            image
            description
            enabled
            url
            client
            user
            oAuthUrl
            wxappLogo
        }
    }
}
''',
    'UpdateEmailProvider': '''
mutation UpdateEmailProvider($options: EmailProviderListInput){
    UpdateEmailProvider(options: $options){
        _id
        name
        image
        description
        fields{
            label
            type
            placeholder
            help
            value
            options
        }
        client
        user
        status
        provider{
            _id
            name
            image
            description
            client
            user
            status
        }
    }
}
''',
    'UpdateEmailTemplate': '''
mutation UpdateEmailTemplate($options: EmailTemplateInput!){
    UpdateEmailTemplate(options: $options){
        _id
        type
        sender
        object
        hasURL
        URLExpireTime
        status
        redirectTo
        content
    }
}
''',
    'UpdateEmailTemplateWithClient': '''
mutation UpdateEmailTemplateWithClient($options: EmailTemplateWithClientInput!){
    UpdateEmailTemplateWithClient(options: $options){
        _id
        user
        client
        status
        fields{
            label
            type
            placeholder
            help
            value
            options
        }
        provider{
            _id
            name
            image
            description
        }
    }
}
''',
    'UpdateLDAPServer': '''
mutation UpdateLDAPServer($ldapId: String!, $name: String!, $clientId: String!, $userId: String!, $ldapLink: String!, $baseDN: String!, $username: String!, $searchStandard: String!, $password: String!, $emailPostfix: String, $description: String, $enabled: Boolean){
    UpdateLDAPServer(ldapId: $ldapId, name: $name, clientId: $clientId, userId: $userId, ldapLink: $ldapLink, baseDN: $baseDN, username: $username, searchStandard: $searchStandard, password: $password, emailPostfix: $emailPostfix, description: $description, enabled: $enabled){
        _id
        name
        clientId
        userId
        ldapLink
        baseDN
        searchStandard
        emailPostfix
        username
        password
        description
        enabled
        isDeleted
        createdAt
        updatedAt
    }
}
''',
    'UpdateOAuthList': '''
mutation UpdateOAuthList($options: OAuthListUpdateInput, $fields: [OAuthListFieldsFormUpdateInput]){
    UpdateOAuthList(options: $options, fields: $fields){
        _id
        name
        alias
        image
        description
        enabled
        url
        client
        user
        oAuthUrl
        wxappLogo
        fields{
            label
            type
            placeholder
            value
            checked
        }
        oauth{
            _id
            name
            alias
            image
            description
            enabled
            url
            client
            user
            oAuthUrl
            wxappLogo
        }
    }
}
''',
    'UpdateOAuthProvider': '''
mutation UpdateOAuthProvider($appId: String!, $domain: String, $name: String, $image: String, $redirectUris: [String], $grants: [String], $description: String, $homepageURL: String, $css: String, $casExpire: Int){
    UpdateOAuthProvider(appId: $appId, domain: $domain, name: $name, image: $image, redirectUris: $redirectUris, grants: $grants, description: $description, homepageURL: $homepageURL, css: $css, casExpire: $casExpire){
        _id
        name
        domain
        image
        redirectUris
        appSecret
        client_id
        clientId
        grants
        description
        homepageURL
        isDeleted
        when
        css
        loginUrl
        casExpire
    }
}
''',
    'UpdateOIDCApp': '''
mutation UpdateOIDCApp($appId: String!, $domain: String, $name: String, $image: String, $redirect_uris: [String], $token_endpoint_auth_method: String, $grant_types: [String], $response_types: [String], $id_token_signed_response_alg: String, $id_token_encrypted_response_alg: String, $id_token_encrypted_response_enc: String, $userinfo_signed_response_alg: String, $userinfo_encrypted_response_alg: String, $userinfo_encrypted_response_enc: String, $request_object_signing_alg: String, $request_object_encryption_alg: String, $request_object_encryption_enc: String, $jwks_uri: String, $_jwks_uri: String, $custom_jwks: String, $jwks: String, $_jwks: String, $description: String, $homepageURL: String, $css: String, $authorization_code_expire: String, $id_token_expire: String, $access_token_expire: String, $cas_expire: String, $customStyles: OIDCProviderCustomStylesInput){
    UpdateOIDCApp(appId: $appId, domain: $domain, name: $name, image: $image, redirect_uris: $redirect_uris, token_endpoint_auth_method: $token_endpoint_auth_method, grant_types: $grant_types, response_types: $response_types, id_token_signed_response_alg: $id_token_signed_response_alg, id_token_encrypted_response_alg: $id_token_encrypted_response_alg, id_token_encrypted_response_enc: $id_token_encrypted_response_enc, userinfo_signed_response_alg: $userinfo_signed_response_alg, userinfo_encrypted_response_alg: $userinfo_encrypted_response_alg, userinfo_encrypted_response_enc: $userinfo_encrypted_response_enc, request_object_signing_alg: $request_object_signing_alg, request_object_encryption_alg: $request_object_encryption_alg, request_object_encryption_enc: $request_object_encryption_enc, jwks_uri: $jwks_uri, _jwks_uri: $_jwks_uri, custom_jwks: $custom_jwks, jwks: $jwks, _jwks: $_jwks, description: $description, homepageURL: $homepageURL, css: $css, authorization_code_expire: $authorization_code_expire, id_token_expire: $id_token_expire, access_token_expire: $access_token_expire, cas_expire: $cas_expire, customStyles: $customStyles){
        _id
        name
        domain
        image
        redirect_uris
        client_id
        client_secret
        token_endpoint_auth_method
        id_token_signed_response_alg
        id_token_encrypted_response_alg
        id_token_encrypted_response_enc
        userinfo_signed_response_alg
        userinfo_encrypted_response_alg
        userinfo_encrypted_response_enc
        request_object_signing_alg
        request_object_encryption_alg
        request_object_encryption_enc
        jwks_uri
        _jwks_uri
        custom_jwks
        jwks
        _jwks
        clientId
        grant_types
        response_types
        description
        homepageURL
        isDeleted
        isDefault
        when
        css
        authorization_code_expire
        id_token_expire
        access_token_expire
        cas_expire
        loginUrl
        customStyles{
            forceLogin
            hideQRCode
            hideUP
            hideUsername
            hideRegister
            hidePhone
            hideSocial
            hideClose
            hidePhonePassword
            defaultLoginMethod
        }
    }
}
''',
    'UpdateSAMLIdentityProvider': '''
mutation UpdateSAMLIdentityProvider($appId: String!, $clientId: String!, $domain: String, $image: String, $name: String, $description: String, $SPMetadata: String, $attributeNameFormat: String, $customAttributes: String, $emailDomainTransformation: String, $authnContextClassRef: String, $IdPMetadata: String, $assertionConsumerUrl: String, $bindings: [String], $nameIds: [String], $attributes: [String], $enableSignRes: Boolean, $resSignAlgorithm: String, $resAbstractAlgorithm: String, $resSignPublicKey: String, $resSignPrivateKey: String, $resSignPrivateKeyPass: String, $enableSignReq: Boolean, $reqSignPublicKey: String, $enableEncryptRes: Boolean, $resEncryptPublicKey: String, $css: String){
    UpdateSAMLIdentityProvider(appId: $appId, clientId: $clientId, domain: $domain, image: $image, name: $name, description: $description, SPMetadata: $SPMetadata, attributeNameFormat: $attributeNameFormat, customAttributes: $customAttributes, emailDomainTransformation: $emailDomainTransformation, authnContextClassRef: $authnContextClassRef, IdPMetadata: $IdPMetadata, assertionConsumerUrl: $assertionConsumerUrl, bindings: $bindings, nameIds: $nameIds, attributes: $attributes, enableSignRes: $enableSignRes, resSignAlgorithm: $resSignAlgorithm, resAbstractAlgorithm: $resAbstractAlgorithm, resSignPublicKey: $resSignPublicKey, resSignPrivateKey: $resSignPrivateKey, resSignPrivateKeyPass: $resSignPrivateKeyPass, enableSignReq: $enableSignReq, reqSignPublicKey: $reqSignPublicKey, enableEncryptRes: $enableEncryptRes, resEncryptPublicKey: $resEncryptPublicKey, css: $css){
        _id
        name
        domain
        image
        appSecret
        appId
        clientId
        description
        isDeleted
        enabled
        when
        SPMetadata
        attributeNameFormat
        customAttributes
        emailDomainTransformation
        authnContextClassRef
        IdPMetadata
        assertionConsumerUrl
        bindings
        nameIds
        attributes
        enableSignRes
        resSignAlgorithm
        resAbstractAlgorithm
        resSignPublicKey
        resSignPrivateKey
        resSignPrivateKeyPass
        enableSignReq
        reqSignPublicKey
        enableEncryptRes
        resEncryptPublicKey
        css
    }
}
''',
    'UpdateSAMLServiceProvider': '''
mutation UpdateSAMLServiceProvider($appId: String!, $name: String!, $domain: String!, $clientId: String!, $redirectUrl: String!, $loginUrl: String!, $logoutUrl: String!, $nameId: String!, $IdPEntityID: String, $assertionConsumeService: [AssertionConsumeServiceInputType], $image: String, $mappings: AssertionMapInputType, $defaultIdPMapId: String, $description: String, $SPMetadata: String, $IdPMetadata: String, $enableSignRes: Boolean, $resSignPublicKey: String, $hasResEncrypted: Boolean, $resEncryptAlgorithm: String, $resAbstractAlgorithm: String, $resDecryptPrivateKey: String, $resDecryptPrivateKeyPass: String, $resEncryptPublicKey: String, $enableSignReq: Boolean, $reqSignAlgorithm: String, $reqAbstractAlgorithm: String, $reqSignPrivateKey: String, $reqSignPrivateKeyPass: String, $reqSignPublicKey: String){
    UpdateSAMLServiceProvider(appId: $appId, name: $name, domain: $domain, clientId: $clientId, redirectUrl: $redirectUrl, loginUrl: $loginUrl, logoutUrl: $logoutUrl, nameId: $nameId, IdPEntityID: $IdPEntityID, assertionConsumeService: $assertionConsumeService, image: $image, mappings: $mappings, defaultIdPMapId: $defaultIdPMapId, description: $description, SPMetadata: $SPMetadata, IdPMetadata: $IdPMetadata, enableSignRes: $enableSignRes, resSignPublicKey: $resSignPublicKey, hasResEncrypted: $hasResEncrypted, resEncryptAlgorithm: $resEncryptAlgorithm, resAbstractAlgorithm: $resAbstractAlgorithm, resDecryptPrivateKey: $resDecryptPrivateKey, resDecryptPrivateKeyPass: $resDecryptPrivateKeyPass, resEncryptPublicKey: $resEncryptPublicKey, enableSignReq: $enableSignReq, reqSignAlgorithm: $reqSignAlgorithm, reqAbstractAlgorithm: $reqAbstractAlgorithm, reqSignPrivateKey: $reqSignPrivateKey, reqSignPrivateKeyPass: $reqSignPrivateKeyPass, reqSignPublicKey: $reqSignPublicKey){
        _id
        name
        domain
        image
        appSecret
        defaultIdPMap{
            _id
            name
            image
            description
            isDeleted
        }
        defaultIdPMapId
        appId
        clientId
        description
        isDeleted
        enabled
        when
        SPMetadata
        IdPMetadata
        IdPEntityID
        assertionConsumeService{
            binding
            url
            isDefault
        }
        mappings{
            username
            nickname
            photo
            company
            providerName
            email
        }
        redirectUrl
        loginUrl
        logoutUrl
        nameId
        enableSignRes
        resSignPublicKey
        hasResEncrypted
        resEncryptAlgorithm
        resAbstractAlgorithm
        resDecryptPrivateKey
        resDecryptPrivateKeyPass
        resEncryptPublicKey
        enableSignReq
        reqSignAlgorithm
        reqAbstractAlgorithm
        reqSignPrivateKey
        reqSignPrivateKeyPass
        reqSignPublicKey
        SPUrl
    }
}
''',
    'UpdateSystemPricing': '''
mutation UpdateSystemPricing($options: PricingFieldsInput){
    UpdateSystemPricing(options: $options){
        _id
        type
        startNumber
        freeNumber
        startPrice
        maxNumber
        d
        features
    }
}
''',
    'UseDefaultEmailProvider': '''
mutation UseDefaultEmailProvider($user: String!, $client: String!){
    UseDefaultEmailProvider(user: $user, client: $client)
}
''',
    'addClientWebhook': '''
mutation addClientWebhook(
  $client: String!
  $events: [String!]!
  $url: String!
  $contentType: String!
  $enable: Boolean!
  $secret: String
  $isLastTimeSuccess: Boolean
) {
  addClientWebhook(
    client: $client
    events: $events
    url: $url
    contentType: $contentType
    enable: $enable
    secret: $secret
    isLastTimeSuccess: $isLastTimeSuccess
  ) {
    _id
    client
    events {
      name
      label
      description
    }
    url
    isLastTimeSuccess
    contentType
    secret
    enable
  }
}

''',
    'addCollaborator': '''
mutation addCollaborator(
  $userPoolId: String!
  $collaboratorUserId: String!
  $permissionDescriptors: [PermissionDescriptorsInputType]!
) {
  addCollaborator(
    userPoolId: $userPoolId
    collaboratorUserId: $collaboratorUserId
    permissionDescriptors: $permissionDescriptors
  ) {
    _id
  }
}

''',
    'addGroupMetadata': '''
mutation addGroupMetadata($groupId: String!, $key: String!, $value: String!) {
  addGroupMetadata(groupId: $groupId, key: $key, value: $value) {
    key
    value
  }
}

''',
    'addOrgNode': '''
mutation addOrgNode($input: AddOrgNodeInput!){
    addOrgNode(input: $input){
        _id
        nodes{
            _id
            name
            description
            createdAt
            updatedAt
            children
            root
        }
    }
}
''',
    'addPermission': '''
mutation addPermission($name: String!, $description: String){
    addPermission(name: $name, description: $description){
        _id
        name
        affect
        description
    }
}
''',
    'addPermissionToRBACRole': '''
mutation addPermissionToRBACRole($sortBy: SortByEnum, $page: Int, $count: Int, $input: AddPermissionToRBACRoleInput!){
    addPermissionToRBACRole(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'addPermissionToRBACRoleBatch': '''
mutation addPermissionToRBACRoleBatch($sortBy: SortByEnum, $page: Int, $count: Int, $input: AddPermissionToRBACRoleBatchInput){
    addPermissionToRBACRoleBatch(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'addRoleToRBACGroup': '''
mutation addRoleToRBACGroup($sortBy: SortByEnum, $page: Int, $count: Int, $input: AddRoleToRBACGroupInput!){
    addRoleToRBACGroup(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        roles{
            totalCount
        }
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'addRoleToRBACGroupBatch': '''
mutation addRoleToRBACGroupBatch($sortBy: SortByEnum, $page: Int, $count: Int, $input: AddRoleToRBACGroupBatchInput!){
    addRoleToRBACGroupBatch(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        roles{
            totalCount
        }
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'addSuperAdminUser': '''
mutation addSuperAdminUser($options: SuperAdminUpdateInput!){
    addSuperAdminUser(options: $options){
        email
        username
        _id
        upgrade
    }
}
''',
    'addToInvitation': '''
mutation addToInvitation($client: String!, $phone: String){
    addToInvitation(client: $client, phone: $phone){
        client
        phone
        isDeleted
        createdAt
        updatedAt
    }
}
''',
    'addUserToRBACGroup': '''
mutation addUserToRBACGroup($sortBy: SortByEnum, $page: Int, $count: Int, $input: AddUserToRBACGroupInput!){
    addUserToRBACGroup(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        roles{
            totalCount
        }
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'addUserToRBACGroupBatch': '''
mutation addUserToRBACGroupBatch($sortBy: SortByEnum, $page: Int, $count: Int, $input: AddUserToRBACGroupBatchInput!){
    addUserToRBACGroupBatch(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        roles{
            totalCount
        }
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'assignRBACRoleToUser': '''
mutation assignRBACRoleToUser($sortBy: SortByEnum, $page: Int, $count: Int, $input: AssignUserToRBACRoleInput!){
    assignRBACRoleToUser(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'assignRBACRoleToUserBatch': '''
mutation assignRBACRoleToUserBatch($sortBy: SortByEnum, $page: Int, $count: Int, $input: AssignUserToRBACRoleBatchInput!){
    assignRBACRoleToUserBatch(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'assignUserToRole': '''
mutation assignUserToRole($client: String!, $user: String!, $group: String!){
    assignUserToRole(client: $client, user: $user, group: $group){
        list{
            _id
            createdAt
        }
        totalCount
    }
}
''',
    'bindOtherOAuth': '''
mutation bindOtherOAuth($type: String!, $unionid: String!, $userInfo: String!, $client: String, $user: String){
    bindOtherOAuth(type: $type, unionid: $unionid, userInfo: $userInfo, client: $client, user: $user){
        _id
        user
        client
        type
        unionid
        userInfo
        createdAt
    }
}
''',
    'changeMFA': '''
mutation changeMFA($enable: Boolean!, $userId: String, $userPoolId: String, $_id: String, $refreshKey: Boolean){
    changeMFA(enable: $enable, userId: $userId, userPoolId: $userPoolId, _id: $_id, refreshKey: $refreshKey){
        _id
        userId
        userPoolId
        enable
        shareKey
    }
}
''',
    'changePassword': '''
mutation changePassword($password: String!, $email: String!, $client: String!, $verifyCode: String!){
    changePassword(password: $password, email: $email, client: $client, verifyCode: $verifyCode){
        _id
        email
        unionid
        openid
        emailVerified
        phone
        phoneVerified
        username
        nickname
        company
        photo
        browser
        device
        password
        registerInClient
        registerMethod
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        country
        updatedAt
        group{
            _id
            name
            descriptions
            client
            permissions
            createdAt
        }
        clientType{
            _id
            name
            description
            image
            example
        }
        userLocation{
            _id
            when
            where
        }
        userLoginHistory{
            totalCount
        }
        systemApplicationType{
            _id
            name
            descriptions
            price
        }
        thirdPartyIdentity{
            provider
            refreshToken
            accessToken
            expiresIn
            updatedAt
        }
        customData
        metadata
    }
}
''',
    'createAdConnector': '''
mutation createAdConnector($name: String!, $logo: String, $userPoolId: String!){
    createAdConnector(name: $name, logo: $logo, userPoolId: $userPoolId){
        _id
        name
        secret
        salt
        logo
        enabled
        userPoolId
        status
        createdAt
    }
}
''',
    'createCustomMFA': '''
mutation createCustomMFA($userIdInMiniLogin: String!, $userPoolId: String!, $name: String!, $secret: String!, $remark: String){
    createCustomMFA(userIdInMiniLogin: $userIdInMiniLogin, userPoolId: $userPoolId, name: $name, secret: $secret, remark: $remark){
        _id
        userIdInMiniLogin
        userPoolId{
            _id
            usersCount
            logo
            emailVerifiedDefault
            sendWelcomeEmail
            registerDisabled
            showWXMPQRCode
            useMiniLogin
            useSelfWxapp
            allowedOrigins
            name
            secret
            token
            descriptions
            jwtExpired
            createdAt
            isDeleted
            enableEmail
        }
        remark
        name
        secret
    }
}
''',
    'createInterConnection': '''
mutation createInterConnection(
  $sourceUserPoolId: String!
  $sourceUserId: String!
  $targetUserPoolId: String!
  $targetUserId: String!
  $maxAge: Int!
) {
  createInterConnection(
    sourceUserPoolId: $sourceUserPoolId
    sourceUserId: $sourceUserId
    targetUserId: $targetUserId
    targetUserPoolId: $targetUserPoolId
    maxAge: $maxAge
  ) {
    message
    code
    status
  }
}

''',
    'createOrg': '''
mutation createOrg($input: CreateOrgInput!){
    createOrg(input: $input){
        _id
        nodes{
            _id
            name
            description
            createdAt
            updatedAt
            children
            root
        }
    }
}
''',
    'createRBACGroup': '''
mutation createRBACGroup($input: CreateRBACGroupInput!){
    createRBACGroup(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
    }
}
''',
    'createRBACPermission': '''
mutation createRBACPermission($input: CreateRBACPermissionInput!){
    createRBACPermission(input: $input){
        _id
        name
        userPoolId
        createdAt
        updatedAt
        description
    }
}
''',
    'createRBACRole': '''
mutation createRBACRole($sortBy: SortByEnum, $page: Int, $count: Int, $input: CreateRBACRoleInput!){
    createRBACRole(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'createRole': '''
mutation createRole($client: String!, $name: String!, $descriptions: String){
    createRole(client: $client, name: $name, descriptions: $descriptions){
        _id
        name
        descriptions
        client
        permissions
        createdAt
    }
}
''',
    'createRule': '''
mutation createRule($input: CreateRuleInput!){
    createRule(input: $input){
        _id
        userPoolId
        name
        description
        type
        enabled
        faasUrl
        code
        order
        async
        createdAt
        updatedAt
    }
}
''',
    'createUser': '''
mutation createUser($userInfo: UserRegisterInput!, $invitationCode: String, $keepPassword: Boolean){
    createUser(userInfo: $userInfo, invitationCode: $invitationCode, keepPassword: $keepPassword){
        _id
        email
        unionid
        openid
        emailVerified
        phone
        phoneVerified
        username
        nickname
        company
        photo
        browser
        device
        password
        registerInClient
        registerMethod
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        country
        updatedAt
        group{
            _id
            name
            descriptions
            client
            permissions
            createdAt
        }
        clientType{
            _id
            name
            description
            image
            example
        }
        userLocation{
            _id
            when
            where
        }
        userLoginHistory{
            totalCount
        }
        systemApplicationType{
            _id
            name
            descriptions
            price
        }
        thirdPartyIdentity{
            provider
            refreshToken
            accessToken
            expiresIn
            updatedAt
        }
        customData
        metadata
    }
}
''',
    'createUserWithoutAuthentication': '''
mutation createUserWithoutAuthentication(
  $userPoolId: String!
  $userInfo: UserRegisterInput!
  $forceLogin: Boolean
) {
  createUserWithoutAuthentication(
    userPoolId: $userPoolId
    userInfo: $userInfo
    forceLogin: $forceLogin
  ) {
    _id
    email
    unionid
    openid
    emailVerified
    phone
    phoneVerified
    username
    nickname
    company
    photo
    browser
    device
    password
    registerInClient
    registerMethod
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    country
    updatedAt
    metadata
  }
}

''',
    'deleteClientWebhook': '''
mutation deleteClientWebhook($id: String!){
    deleteClientWebhook(id: $id){
        _id
        client
        events{
            name
            label
            description
        }
        url
        isLastTimeSuccess
        contentType
        secret
        enable
    }
}
''',
    'deleteOrg': '''
mutation deleteOrg($_id: String!){
    deleteOrg(_id: $_id){
        message
        code
        status
    }
}
''',
    'deleteRBACGroup': '''
mutation deleteRBACGroup($_id: String!){
    deleteRBACGroup(_id: $_id){
        message
        code
        status
    }
}
''',
    'deleteRBACGroupBatch': '''
mutation deleteRBACGroupBatch($idList: [String!]!){
    deleteRBACGroupBatch(idList: $idList){
        message
        code
        status
    }
}
''',
    'deleteRBACPermission': '''
mutation deleteRBACPermission($_id: String!){
    deleteRBACPermission(_id: $_id){
        message
        code
        status
    }
}
''',
    'deleteRBACPermissionBatch': '''
mutation deleteRBACPermissionBatch($idList: [String!]!){
    deleteRBACPermissionBatch(idList: $idList){
        message
        code
        status
    }
}
''',
    'deleteRBACRole': '''
mutation deleteRBACRole($_id: String!){
    deleteRBACRole(_id: $_id){
        message
        code
        status
    }
}
''',
    'deleteRBACRoleBatch': '''
mutation deleteRBACRoleBatch($idList: [String!]!){
    deleteRBACRoleBatch(idList: $idList){
        message
        code
        status
    }
}
''',
    'deleteRule': '''
mutation deleteRule($_id: String!){
    deleteRule(_id: $_id){
        message
        code
        status
    }
}
''',
    'disableAdConnector': '''
mutation disableAdConnector($_id: String!){
    disableAdConnector(_id: $_id)
}
''',
    'disableAdConnectorForProvider': '''
mutation disableAdConnectorForProvider($providerId: String!, $adConnectorId: String!){
    disableAdConnectorForProvider(providerId: $providerId, adConnectorId: $adConnectorId)
}
''',
    'enableAdConnector': '''
mutation enableAdConnector($_id: String!){
    enableAdConnector(_id: $_id)
}
''',
    'enableAdConnectorForProvider': '''
mutation enableAdConnectorForProvider($providerType: providerType!, $providerId: String!, $adConnectorId: String!){
    enableAdConnectorForProvider(providerType: $providerType, providerId: $providerId, adConnectorId: $adConnectorId)
}
''',
    'enablePasswordFaas': '''
mutation enablePasswordFaas($client: String!, $enable: Boolean!){
    enablePasswordFaas(client: $client, enable: $enable){
        encryptUrl
        decryptUrl
        user
        client
        logs
        enable
        createdAt
        updatedAt
    }
}
''',
    'encryptPassword': '''
mutation encryptPassword($password: String!, $client: String!, $isTest: Boolean){
    encryptPassword(password: $password, client: $client, isTest: $isTest){
        _id
        encryptUrl
        decryptUrl
        client
        user
        logs
        enable
        createdAt
        updatedAt
        password
    }
}
''',
    'generateInvitationCode': '''
mutation generateInvitationCode($user: String!, $client: String!){
    generateInvitationCode(user: $user, client: $client){
        _id
        user
        client
        code
        createdAt
    }
}
''',
    'login': '''
mutation login($registerInClient: String!, $phone: String, $phoneCode: Int, $unionid: String, $openid: String, $username: String, $email: String, $password: String, $lastIP: String, $verifyCode: String, $MFACode: String, $fromRegister: Boolean, $device: String, $browser: String){
    login(registerInClient: $registerInClient, phone: $phone, phoneCode: $phoneCode, unionid: $unionid, openid: $openid, username: $username, email: $email, password: $password, lastIP: $lastIP, verifyCode: $verifyCode, MFACode: $MFACode, fromRegister: $fromRegister, device: $device, browser: $browser){
        _id
        email
        unionid
        openid
        emailVerified
        phone
        phoneVerified
        username
        nickname
        company
        photo
        browser
        device
        password
        registerInClient
        registerMethod
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        country
        updatedAt
        group{
            _id
            name
            descriptions
            client
            permissions
            createdAt
        }
        clientType{
            _id
            name
            description
            image
            example
        }
        userLocation{
            _id
            when
            where
        }
        userLoginHistory{
            totalCount
        }
        systemApplicationType{
            _id
            name
            descriptions
            price
        }
        thirdPartyIdentity{
            provider
            refreshToken
            accessToken
            expiresIn
            updatedAt
        }
        customData
        metadata
    }
}
''',
    'loginByAd': '''
mutation loginByAd($adConnectorId: String!, $username: String!, $password: String!){
    loginByAd(adConnectorId: $adConnectorId, username: $username, password: $password){
        _id
        username
        email
        unionid
        openid
        emailVerified
        phone
        phoneVerified
        nickname
        company
        photo
        browser
        password
        registerInClient
        registerMethod
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        device
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        country
        updatedAt
        thirdPartyIdentity{
            provider
            refreshToken
            accessToken
            expiresIn
            updatedAt
        }
        oldPassword
        metadata
    }
}
''',
    'loginByEmail': '''
mutation loginByEmail($clientId: String!, $email: String, $password: String) {
  login(registerInClient: $clientId, email: $email, password: $password) {
    _id
    email
    unionid
    openid
    emailVerified
    phone
    phoneVerified
    username
    nickname
    company
    photo
    browser
    device
    password
    registerInClient
    registerMethod
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    country
    updatedAt
    group {
      _id
      name
      descriptions
      client
      permissions
      createdAt
    }
    clientType {
      _id
      name
      description
      image
      example
    }
    userLocation {
      _id
      when
      where
    }
    userLoginHistory {
      totalCount
    }
    systemApplicationType {
      _id
      name
      descriptions
      price
    }
    thirdPartyIdentity {
      provider
      refreshToken
      accessToken
      expiresIn
      updatedAt
    }
    customData
    metadata
  }
}

''',
    'loginByPhoneCode': '''
mutation loginByPhoneCode($clientId: String!, $phone: String, $phoneCode: Int) {
  login(registerInClient: $clientId, phone: $phone, phoneCode: $phoneCode) {
    _id
    email
    unionid
    openid
    emailVerified
    phone
    phoneVerified
    username
    nickname
    company
    photo
    browser
    device
    password
    registerInClient
    registerMethod
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    country
    updatedAt
    group {
      _id
      name
      descriptions
      client
      permissions
      createdAt
    }
    clientType {
      _id
      name
      description
      image
      example
    }
    userLocation {
      _id
      when
      where
    }
    userLoginHistory {
      totalCount
    }
    systemApplicationType {
      _id
      name
      descriptions
      price
    }
    thirdPartyIdentity {
      provider
      refreshToken
      accessToken
      expiresIn
      updatedAt
    }
    customData
    metadata
  }
}

''',
    'loginByPhonePassword': '''
mutation loginByPhonePassword($clientId: String!, $phone: String, $password: String) {
  login(registerInClient: $clientId, phone: $phone, password: $password) {
    _id
    email
    unionid
    openid
    emailVerified
    phone
    phoneVerified
    username
    nickname
    company
    photo
    browser
    device
    password
    registerInClient
    registerMethod
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    country
    updatedAt
    group {
      _id
      name
      descriptions
      client
      permissions
      createdAt
    }
    clientType {
      _id
      name
      description
      image
      example
    }
    userLocation {
      _id
      when
      where
    }
    userLoginHistory {
      totalCount
    }
    systemApplicationType {
      _id
      name
      descriptions
      price
    }
    thirdPartyIdentity {
      provider
      refreshToken
      accessToken
      expiresIn
      updatedAt
    }
    customData
    metadata
  }
}

''',
    'loginByUsername': '''
mutation loginByUsername($clientId: String!, $username: String, $password: String) {
  login(registerInClient: $clientId, username: $username, password: $password) {
    _id
    email
    unionid
    openid
    emailVerified
    phone
    phoneVerified
    username
    nickname
    company
    photo
    browser
    device
    password
    registerInClient
    registerMethod
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    country
    updatedAt
    group {
      _id
      name
      descriptions
      client
      permissions
      createdAt
    }
    clientType {
      _id
      name
      description
      image
      example
    }
    userLocation {
      _id
      when
      where
    }
    userLoginHistory {
      totalCount
    }
    systemApplicationType {
      _id
      name
      descriptions
      price
    }
    thirdPartyIdentity {
      provider
      refreshToken
      accessToken
      expiresIn
      updatedAt
    }
    customData
    metadata
  }
}

''',
    'newClient': '''
mutation newClient($client: NewUserClientInput!){
    newClient(client: $client){
        _id
        user{
            _id
            username
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            nickname
            company
            photo
            browser
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            device
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            oldPassword
            metadata
        }
        clientType{
            _id
            name
            description
            image
            example
        }
        userPoolTypes{
            _id
            name
            description
            image
            example
        }
        usersCount
        logo
        emailVerifiedDefault
        sendWelcomeEmail
        registerDisabled
        showWXMPQRCode
        useMiniLogin
        useSelfWxapp
        allowedOrigins
        name
        secret
        token
        descriptions
        jwtExpired
        createdAt
        isDeleted
        frequentRegisterCheck{
            timeInterval
            limit
            enable
        }
        loginFailCheck{
            timeInterval
            limit
            enable
        }
        enableEmail
        changePhoneStrategy{
            verifyOldPhone
        }
        changeEmailStrategy{
            verifyOldEmail
        }
        qrcodeLoginStrategy{
            qrcodeExpiresAfter
            returnFullUserInfo
            allowExchangeUserInfoFromBrowser
            ticketExpiresAfter
        }
        app2WxappLoginStrategy{
            ticketExpriresAfter
            ticketExchangeUserInfoNeedSecret
        }
    }
}
''',
    'oauthPasswordLogin': '''
mutation oauthPasswordLogin($registerInClient: String!, $phone: String, $unionid: String, $email: String, $password: String, $lastIP: String, $verifyCode: String){
    oauthPasswordLogin(registerInClient: $registerInClient, phone: $phone, unionid: $unionid, email: $email, password: $password, lastIP: $lastIP, verifyCode: $verifyCode){
        _id
        email
        unionid
        openid
        emailVerified
        phone
        phoneVerified
        username
        nickname
        company
        photo
        browser
        device
        password
        registerInClient
        registerMethod
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        country
        updatedAt
        group{
            _id
            name
            descriptions
            client
            permissions
            createdAt
        }
        clientType{
            _id
            name
            description
            image
            example
        }
        userLocation{
            _id
            when
            where
        }
        userLoginHistory{
            totalCount
        }
        systemApplicationType{
            _id
            name
            descriptions
            price
        }
        thirdPartyIdentity{
            provider
            refreshToken
            accessToken
            expiresIn
            updatedAt
        }
        customData
        metadata
    }
}
''',
    'order': '''
mutation order($options: OrderAddInput!){
    order(options: $options){
        code
        url
        charge
    }
}
''',
    'passwordLessForceLogin': '''
mutation passwordLessForceLogin($userPoolId: String!, $userId: String!) {
  passwordLessForceLogin(userPoolId: $userPoolId, userId: $userId) {
    _id
    email
    unionid
    openid
    emailVerified
    phone
    phoneVerified
    username
    nickname
    company
    photo
    browser
    device
    password
    registerInClient
    registerMethod
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    country
    updatedAt
    metadata
  }
}

''',
    'recordAuthAudit': '''
mutation recordAuthAudit($userPoolId: String!, $appType: String!, $appId: String!, $userId: String!, $event: String!, $message: String){
    recordAuthAudit(userPoolId: $userPoolId, appType: $appType, appId: $appId, userId: $userId, event: $event, message: $message){
        message
        code
        status
    }
}
''',
    'recordRequest': '''
mutation recordRequest($when: String!, $ip: String!, $responseTime: Int!, $size: Int!, $from: String){
    recordRequest(when: $when, ip: $ip, responseTime: $responseTime, size: $size, from: $from){
        message
        code
        status
    }
}
''',
    'refreshAdConnectorSecret': '''
mutation refreshAdConnectorSecret($_id: String){
    refreshAdConnectorSecret(_id: $_id){
        _id
        name
        secret
        salt
        logo
        enabled
        userPoolId
        status
        createdAt
    }
}
''',
    'refreshAppSecret': '''
mutation refreshAppSecret($client: UpdateUserClientInput!){
    refreshAppSecret(client: $client){
        _id
        user{
            _id
            username
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            nickname
            company
            photo
            browser
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            device
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            oldPassword
            metadata
        }
        clientType{
            _id
            name
            description
            image
            example
        }
        userPoolTypes{
            _id
            name
            description
            image
            example
        }
        usersCount
        logo
        emailVerifiedDefault
        sendWelcomeEmail
        registerDisabled
        showWXMPQRCode
        useMiniLogin
        useSelfWxapp
        allowedOrigins
        name
        secret
        token
        descriptions
        jwtExpired
        createdAt
        isDeleted
        frequentRegisterCheck{
            timeInterval
            limit
            enable
        }
        loginFailCheck{
            timeInterval
            limit
            enable
        }
        enableEmail
        changePhoneStrategy{
            verifyOldPhone
        }
        changeEmailStrategy{
            verifyOldEmail
        }
        qrcodeLoginStrategy{
            qrcodeExpiresAfter
            returnFullUserInfo
            allowExchangeUserInfoFromBrowser
            ticketExpiresAfter
        }
        app2WxappLoginStrategy{
            ticketExpriresAfter
            ticketExchangeUserInfoNeedSecret
        }
    }
}
''',
    'refreshSignInToken': '''
mutation refreshSignInToken($oidcAppId: String, $userPoolId: String, $refreshToken: String!){
    refreshSignInToken(oidcAppId: $oidcAppId, userPoolId: $userPoolId, refreshToken: $refreshToken){
        access_token
        id_token
        refresh_token
        scope
        expires_in
    }
}
''',
    'refreshThirdPartyToken': '''
mutation refreshThirdPartyToken($userPoolId: String!, $userId: String!){
    refreshThirdPartyToken(userPoolId: $userPoolId, userId: $userId){
        refreshSuccess
        message
        provider
        refreshToken
        accessToken
        updatedAt
    }
}
''',
    'refreshToken': '''
mutation refreshToken($client: String!, $user: String!){
    refreshToken(client: $client, user: $user){
        token
        iat
        exp
    }
}
''',
    'register': '''
mutation register(
  $userInfo: UserRegisterInput!
  $invitationCode: String
  $keepPassword: Boolean
) {
  register(
    userInfo: $userInfo
    invitationCode: $invitationCode
    keepPassword: $keepPassword
  ) {
    _id
    email
    unionid
    openid
    emailVerified
    phone
    phoneVerified
    username
    nickname
    company
    photo
    browser
    device
    password
    registerInClient
    registerMethod
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
    name
    givenName
    familyName
    middleName
    profile
    preferredUsername
    website
    gender
    birthdate
    zoneinfo
    locale
    address
    formatted
    streetAddress
    locality
    region
    postalCode
    country
    updatedAt
    metadata
  }
}

''',
    'removeAdConnector': '''
mutation removeAdConnector($_id: String!){
    removeAdConnector(_id: $_id)
}
''',
    'removeCollaborator': '''
mutation removeCollaborator($collaborationId: String!){
    removeCollaborator(collaborationId: $collaborationId){
        _id
        createdAt
        owner{
            _id
            username
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            nickname
            company
            photo
            browser
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            device
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            oldPassword
            metadata
        }
        collaborator{
            _id
            username
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            nickname
            company
            photo
            browser
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            device
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            oldPassword
            metadata
        }
        userPool{
            _id
            usersCount
            logo
            emailVerifiedDefault
            sendWelcomeEmail
            registerDisabled
            showWXMPQRCode
            useMiniLogin
            useSelfWxapp
            allowedOrigins
            name
            secret
            token
            descriptions
            jwtExpired
            createdAt
            isDeleted
            enableEmail
        }
        permissionDescriptors{
            permissionId
            name
            operationAllow
        }
    }
}
''',
    'removeCustomMFA': '''
mutation removeCustomMFA($_id: String!){
    removeCustomMFA(_id: $_id){
        _id
        userIdInMiniLogin
        userPoolId{
            _id
            usersCount
            logo
            emailVerifiedDefault
            sendWelcomeEmail
            registerDisabled
            showWXMPQRCode
            useMiniLogin
            useSelfWxapp
            allowedOrigins
            name
            secret
            token
            descriptions
            jwtExpired
            createdAt
            isDeleted
            enableEmail
        }
        remark
        name
        secret
    }
}
''',
    'removeFromInvitation': '''
mutation removeFromInvitation($client: String!, $phone: String){
    removeFromInvitation(client: $client, phone: $phone){
        client
        phone
        isDeleted
        createdAt
        updatedAt
    }
}
''',
    'removeOrgNode': '''
mutation removeOrgNode($input: RemoveOrgNodeInput!){
    removeOrgNode(input: $input){
        _id
        nodes{
            _id
            name
            description
            createdAt
            updatedAt
            children
            root
        }
    }
}
''',
    'removePermissionFromRBACRole': '''
mutation removePermissionFromRBACRole($sortBy: SortByEnum, $page: Int, $count: Int, $input: RemovePermissionFromRBACRoleInput!){
    removePermissionFromRBACRole(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'removePermissionFromRBACRoleBatch': '''
mutation removePermissionFromRBACRoleBatch($sortBy: SortByEnum, $page: Int, $count: Int, $input: RemovePermissionFromRBACRoleBatchInput!){
    removePermissionFromRBACRoleBatch(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'removeRoleFromRBACGroup': '''
mutation removeRoleFromRBACGroup($sortBy: SortByEnum, $page: Int, $count: Int, $input: RemoveRoleFromRBACGroupInput!){
    removeRoleFromRBACGroup(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        roles{
            totalCount
        }
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'removeRoleFromRBACGroupBatch': '''
mutation removeRoleFromRBACGroupBatch($sortBy: SortByEnum, $page: Int, $count: Int, $input: RemoveRoleFromRBACGroupBatchInput!){
    removeRoleFromRBACGroupBatch(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        roles{
            totalCount
        }
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'removeRuleEnv': '''
mutation removeRuleEnv($input: RemoveRuleEnvInput!){
    removeRuleEnv(input: $input){
        totalCount
        list{
            key
            value
        }
    }
}
''',
    'removeSuperAdminUser': '''
mutation removeSuperAdminUser($_id: String!, $username: String!){
    removeSuperAdminUser(_id: $_id, username: $username){
        email
        username
        _id
        upgrade
    }
}
''',
    'removeUserClients': '''
mutation removeUserClients($ids: [String]){
    removeUserClients(ids: $ids){
        _id
        user{
            _id
            username
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            nickname
            company
            photo
            browser
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            device
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            oldPassword
            metadata
        }
        clientType{
            _id
            name
            description
            image
            example
        }
        userPoolTypes{
            _id
            name
            description
            image
            example
        }
        usersCount
        logo
        emailVerifiedDefault
        sendWelcomeEmail
        registerDisabled
        showWXMPQRCode
        useMiniLogin
        useSelfWxapp
        allowedOrigins
        name
        secret
        token
        descriptions
        jwtExpired
        createdAt
        isDeleted
        frequentRegisterCheck{
            timeInterval
            limit
            enable
        }
        loginFailCheck{
            timeInterval
            limit
            enable
        }
        enableEmail
        changePhoneStrategy{
            verifyOldPhone
        }
        changeEmailStrategy{
            verifyOldEmail
        }
        qrcodeLoginStrategy{
            qrcodeExpiresAfter
            returnFullUserInfo
            allowExchangeUserInfoFromBrowser
            ticketExpiresAfter
        }
        app2WxappLoginStrategy{
            ticketExpriresAfter
            ticketExchangeUserInfoNeedSecret
        }
    }
}
''',
    'removeUserFromGroup': '''
mutation removeUserFromGroup($client: String!, $user: String!, $group: String!){
    removeUserFromGroup(client: $client, user: $user, group: $group){
        _id
        user{
            _id
            username
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            nickname
            company
            photo
            browser
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            device
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            oldPassword
            metadata
        }
        client{
            _id
            usersCount
            logo
            emailVerifiedDefault
            sendWelcomeEmail
            registerDisabled
            showWXMPQRCode
            useMiniLogin
            useSelfWxapp
            allowedOrigins
            name
            secret
            token
            descriptions
            jwtExpired
            createdAt
            isDeleted
            enableEmail
        }
        group{
            _id
            name
            descriptions
            client
            permissions
            createdAt
        }
        createdAt
    }
}
''',
    'removeUserFromRBACGroup': '''
mutation removeUserFromRBACGroup($sortBy: SortByEnum, $page: Int, $count: Int, $input: RemoveUserFromRBACGroupInput!){
    removeUserFromRBACGroup(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        roles{
            totalCount
        }
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'removeUserFromRBACGroupBatch': '''
mutation removeUserFromRBACGroupBatch($sortBy: SortByEnum, $page: Int, $count: Int, $input: RemoveUserFromRBACGroupBatchInput!){
    removeUserFromRBACGroupBatch(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        roles{
            totalCount
        }
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'removeUserMetadata': '''
mutation removeUserMetadata($input: RemoveUserMetadataInput!){
    removeUserMetadata(input: $input){
        totalCount
        list{
            key
            value
        }
    }
}
''',
    'removeUsers': '''
mutation removeUsers($ids: [String], $registerInClient: String, $operator: String){
    removeUsers(ids: $ids, registerInClient: $registerInClient, operator: $operator){
        _id
    }
}
''',
    'resetPassword': '''
mutation resetPassword(
  $email: String!
  $clientId: String!
  $password: String!
  $verifyCode: String!
) {
  changePassword(email: $email, client: $clientId, password: $password, verifyCode: $verifyCode) {
    _id
    email
    emailVerified
    username
    nickname
    company
    photo
    browser
    registerInClient
    registerMethod
    oauth
    token
    tokenExpiredAt
    loginsCount
    lastLogin
    lastIP
    signedUp
    blocked
    isDeleted
  }
}

''',
    'resetUserPoolFromWechat': '''
mutation resetUserPoolFromWechat($client: String!, $registerMethod: String!, $limit: Int!){
    resetUserPoolFromWechat(client: $client, registerMethod: $registerMethod, limit: $limit){
        list{
            _id
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            username
            nickname
            company
            photo
            browser
            device
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            customData
            metadata
        }
        totalCount
    }
}
''',
    'revokeRBACRoleFromUser': '''
mutation revokeRBACRoleFromUser($sortBy: SortByEnum, $page: Int, $count: Int, $input: RevokeRBACRoleFromUserInput!){
    revokeRBACRoleFromUser(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'revokeRBACRoleFromUserBatch': '''
mutation revokeRBACRoleFromUserBatch($sortBy: SortByEnum, $page: Int, $count: Int, $input: RevokeRBACRoleFromUserBatchInput!){
    revokeRBACRoleFromUserBatch(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'sendChangeEmailVerifyCode': '''
mutation sendChangeEmailVerifyCode($userPoolId: String!, $email: String!){
    sendChangeEmailVerifyCode(userPoolId: $userPoolId, email: $email){
        message
        code
        status
    }
}
''',
    'sendResetPasswordEmail': '''
mutation sendResetPasswordEmail($client: String!, $email: String!){
    sendResetPasswordEmail(client: $client, email: $email){
        message
        code
        status
    }
}
''',
    'sendVerifyEmail': '''
mutation sendVerifyEmail($email: String!, $client: String!, $token: String){
    sendVerifyEmail(email: $email, client: $client, token: $token){
        message
        code
        status
    }
}
''',
    'setInvitationState': '''
mutation setInvitationState($client: String!, $enablePhone: Boolean){
    setInvitationState(client: $client, enablePhone: $enablePhone){
        client
        enablePhone
        createdAt
        updatedAt
    }
}
''',
    'setRuleEnv': '''
mutation setRuleEnv($input: SetRuleEnvInput!){
    setRuleEnv(input: $input){
        totalCount
        list{
            key
            value
        }
    }
}
''',
    'setUserMetadata': '''
mutation setUserMetadata($input: SetUserMetadataInput!){
    setUserMetadata(input: $input){
        totalCount
        list{
            key
            value
        }
    }
}
''',
    'signIn': '''
mutation signIn($oidcAppId: String, $userPoolId: String, $email: String, $password: String, $phone: String, $unionid: String, $username: String){
    signIn(oidcAppId: $oidcAppId, userPoolId: $userPoolId, email: $email, password: $password, phone: $phone, unionid: $unionid, username: $username){
        sub
        birthdate
        family_name
        gender
        given_name
        locale
        middle_name
        name
        nickname
        picture
        preferred_username
        profile
        updated_at
        website
        zoneinfo
        username
        _id
        company
        browser
        device
        logins_count
        register_method
        blocked
        last_ip
        register_in_userpool
        last_login
        signed_up
        email
        email_verified
        phone_number
        phone_number_verified
        token
        access_token
        id_token
        refresh_token
        expires_in
        token_type
        scope
    }
}
''',
    'unbindEmail': '''
mutation unbindEmail($user: String, $client: String){
    unbindEmail(user: $user, client: $client){
        _id
        username
        email
        unionid
        openid
        emailVerified
        phone
        phoneVerified
        nickname
        company
        photo
        browser
        password
        registerInClient
        registerMethod
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        device
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        country
        updatedAt
        thirdPartyIdentity{
            provider
            refreshToken
            accessToken
            expiresIn
            updatedAt
        }
        oldPassword
        metadata
    }
}
''',
    'unbindOtherOAuth': '''
mutation unbindOtherOAuth($type: String!, $client: String, $user: String){
    unbindOtherOAuth(type: $type, client: $client, user: $user){
        _id
        user
        client
        type
        unionid
        userInfo
        createdAt
    }
}
''',
    'updateAdConnector': '''
mutation updateAdConnector($_id: String!, $name: String, $logo: String){
    updateAdConnector(_id: $_id, name: $name, logo: $logo){
        _id
        name
        secret
        salt
        logo
        enabled
        userPoolId
        status
        createdAt
    }
}
''',
    'updateClientWebhook': '''
mutation updateClientWebhook($id: String!, $events: [String!]!, $url: String!, $contentType: String!, $enable: Boolean!, $secret: String, $isLastTimeSuccess: Boolean){
    updateClientWebhook(id: $id, events: $events, url: $url, contentType: $contentType, enable: $enable, secret: $secret, isLastTimeSuccess: $isLastTimeSuccess){
        _id
        client
        events{
            name
            label
            description
        }
        url
        isLastTimeSuccess
        contentType
        secret
        enable
    }
}
''',
    'updateCollaborator': '''
mutation updateCollaborator($collaborationId: String!, $permissionDescriptors: [PermissionDescriptorsInputType]!){
    updateCollaborator(collaborationId: $collaborationId, permissionDescriptors: $permissionDescriptors){
        _id
        createdAt
        owner{
            _id
            username
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            nickname
            company
            photo
            browser
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            device
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            oldPassword
            metadata
        }
        collaborator{
            _id
            username
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            nickname
            company
            photo
            browser
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            device
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            oldPassword
            metadata
        }
        userPool{
            _id
            usersCount
            logo
            emailVerifiedDefault
            sendWelcomeEmail
            registerDisabled
            showWXMPQRCode
            useMiniLogin
            useSelfWxapp
            allowedOrigins
            name
            secret
            token
            descriptions
            jwtExpired
            createdAt
            isDeleted
            enableEmail
        }
        permissionDescriptors{
            permissionId
            name
            operationAllow
        }
    }
}
''',
    'updateEmail': '''
mutation updateEmail($userPoolId: String!, $email: String!, $emailCode: String!, $oldEmail: String, $oldEmailCode: String){
    updateEmail(userPoolId: $userPoolId, email: $email, emailCode: $emailCode, oldEmail: $oldEmail, oldEmailCode: $oldEmailCode){
        _id
        username
        email
        unionid
        openid
        emailVerified
        phone
        phoneVerified
        nickname
        company
        photo
        browser
        password
        registerInClient
        registerMethod
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        device
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        country
        updatedAt
        thirdPartyIdentity{
            provider
            refreshToken
            accessToken
            expiresIn
            updatedAt
        }
        oldPassword
        metadata
    }
}
''',
    'updatePasswordStrengthSettingsByUserPoolId': '''
mutation updatePasswordStrengthSettingsByUserPoolId($userPoolId: String!, $pwdStrength: Int){
    updatePasswordStrengthSettingsByUserPoolId(userPoolId: $userPoolId, pwdStrength: $pwdStrength){
        userPoolId
        pwdStrength
    }
}
''',
    'updatePermissions': '''
mutation updatePermissions($role: String!, $client: String!, $permissions: String){
    updatePermissions(role: $role, client: $client, permissions: $permissions){
        _id
        name
        descriptions
        client
        permissions
        createdAt
    }
}
''',
    'updatePhone': '''
mutation updatePhone($userPoolId: String!, $phone: String!, $phoneCode: String!, $oldPhone: String, $oldPhoneCode: String){
    updatePhone(userPoolId: $userPoolId, phone: $phone, phoneCode: $phoneCode, oldPhone: $oldPhone, oldPhoneCode: $oldPhoneCode){
        _id
        username
        email
        unionid
        openid
        emailVerified
        phone
        phoneVerified
        nickname
        company
        photo
        browser
        password
        registerInClient
        registerMethod
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        device
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        country
        updatedAt
        thirdPartyIdentity{
            provider
            refreshToken
            accessToken
            expiresIn
            updatedAt
        }
        oldPassword
        metadata
    }
}
''',
    'updateRBACGroup': '''
mutation updateRBACGroup($sortBy: SortByEnum, $page: Int, $count: Int, $input: UpdateRBACGroupInput!){
    updateRBACGroup(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        roles{
            totalCount
        }
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'updateRBACPermission': '''
mutation updateRBACPermission($input: UpdateRBACPermissionInput!){
    updateRBACPermission(input: $input){
        _id
        name
        userPoolId
        createdAt
        updatedAt
        description
    }
}
''',
    'updateRBACRole': '''
mutation updateRBACRole($sortBy: SortByEnum, $page: Int, $count: Int, $input: UpdateRBACRoleInput!){
    updateRBACRole(input: $input){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'updateRole': '''
mutation updateRole($_id: String!, $client: String!, $name: String!, $descriptions: String, $permissions: String){
    updateRole(_id: $_id, client: $client, name: $name, descriptions: $descriptions, permissions: $permissions){
        _id
        name
        descriptions
        client
        permissions
        createdAt
    }
}
''',
    'updateRule': '''
mutation updateRule($input: UpdateRuleInput!){
    updateRule(input: $input){
        _id
        userPoolId
        name
        description
        type
        enabled
        faasUrl
        code
        order
        async
        createdAt
        updatedAt
    }
}
''',
    'updateRuleOrder': '''
mutation updateRuleOrder($input: UpdateRuleOrderInput!){
    updateRuleOrder(input: $input){
        message
        code
        status
    }
}
''',
    'updateSuperAdminUser': '''
mutation updateSuperAdminUser($options: SuperAdminUpdateInput!){
    updateSuperAdminUser(options: $options){
        email
        username
        _id
        upgrade
    }
}
''',
    'updateUser': '''
mutation updateUser($options: UserUpdateInput!){
    updateUser(options: $options){
        _id
        username
        email
        unionid
        openid
        emailVerified
        phone
        phoneVerified
        nickname
        company
        photo
        browser
        password
        registerInClient
        registerMethod
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        device
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        country
        updatedAt
        thirdPartyIdentity{
            provider
            refreshToken
            accessToken
            expiresIn
            updatedAt
        }
        oldPassword
        metadata
    }
}
''',
    'updateUserClient': '''
mutation updateUserClient($client: UpdateUserClientInput!){
    updateUserClient(client: $client){
        _id
        user{
            _id
            username
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            nickname
            company
            photo
            browser
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            device
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            oldPassword
            metadata
        }
        clientType{
            _id
            name
            description
            image
            example
        }
        userPoolTypes{
            _id
            name
            description
            image
            example
        }
        usersCount
        logo
        emailVerifiedDefault
        sendWelcomeEmail
        registerDisabled
        showWXMPQRCode
        useMiniLogin
        useSelfWxapp
        allowedOrigins
        name
        secret
        token
        descriptions
        jwtExpired
        createdAt
        isDeleted
        frequentRegisterCheck{
            timeInterval
            limit
            enable
        }
        loginFailCheck{
            timeInterval
            limit
            enable
        }
        enableEmail
        changePhoneStrategy{
            verifyOldPhone
        }
        changeEmailStrategy{
            verifyOldEmail
        }
        qrcodeLoginStrategy{
            qrcodeExpiresAfter
            returnFullUserInfo
            allowExchangeUserInfoFromBrowser
            ticketExpiresAfter
        }
        app2WxappLoginStrategy{
            ticketExpriresAfter
            ticketExchangeUserInfoNeedSecret
        }
    }
}
''',
    'verifyResetPasswordVerifyCode': '''
mutation verifyResetPasswordVerifyCode($verifyCode: String!, $email: String!, $client: String!){
    verifyResetPasswordVerifyCode(verifyCode: $verifyCode, email: $email, client: $client){
        message
        code
        status
    }
}
''',

    'GetOIDCAppInfo': '''
query GetOIDCAppInfo($appId: String!){
    GetOIDCAppInfo(appId: $appId){
        _id
        name
        domain
        image
        redirect_uris
        client_id
        client_secret
        token_endpoint_auth_method
        id_token_signed_response_alg
        id_token_encrypted_response_alg
        id_token_encrypted_response_enc
        userinfo_signed_response_alg
        userinfo_encrypted_response_alg
        userinfo_encrypted_response_enc
        request_object_signing_alg
        request_object_encryption_alg
        request_object_encryption_enc
        jwks_uri
        _jwks_uri
        custom_jwks
        jwks
        _jwks
        clientId
        grant_types
        response_types
        description
        homepageURL
        isDeleted
        isDefault
        when
        css
        authorization_code_expire
        id_token_expire
        access_token_expire
        cas_expire
        loginUrl
        customStyles{
            forceLogin
            hideQRCode
            hideUP
            hideUsername
            hideRegister
            hidePhone
            hideSocial
            hideClose
            hidePhonePassword
            defaultLoginMethod
        }
    }
}
''',
    'GetOIDCAppList': '''
query GetOIDCAppList($clientId: String, $page: Int, $count: Int){
    GetOIDCAppList(clientId: $clientId, page: $page, count: $count){
        totalCount
        list{
            _id
            name
            domain
            image
            redirect_uris
            client_id
            client_secret
            token_endpoint_auth_method
            id_token_signed_response_alg
            id_token_encrypted_response_alg
            id_token_encrypted_response_enc
            userinfo_signed_response_alg
            userinfo_encrypted_response_alg
            userinfo_encrypted_response_enc
            request_object_signing_alg
            request_object_encryption_alg
            request_object_encryption_enc
            jwks_uri
            _jwks_uri
            custom_jwks
            jwks
            _jwks
            clientId
            grant_types
            response_types
            description
            homepageURL
            isDeleted
            isDefault
            when
            css
            authorization_code_expire
            id_token_expire
            access_token_expire
            cas_expire
            loginUrl
        }
    }
}
''',
    'GetSAMLIdentityProviderInfo': '''
query GetSAMLIdentityProviderInfo($appId: String!){
    GetSAMLIdentityProviderInfo(appId: $appId){
        _id
        name
        domain
        image
        appSecret
        appId
        clientId
        description
        isDeleted
        enabled
        when
        SPMetadata
        attributeNameFormat
        customAttributes
        emailDomainTransformation
        authnContextClassRef
        IdPMetadata
        assertionConsumerUrl
        bindings
        nameIds
        attributes
        enableSignRes
        resSignAlgorithm
        resAbstractAlgorithm
        resSignPublicKey
        resSignPrivateKey
        resSignPrivateKeyPass
        enableSignReq
        reqSignPublicKey
        enableEncryptRes
        resEncryptPublicKey
        css
    }
}
''',
    'GetSAMLIdentityProviderList': '''
query GetSAMLIdentityProviderList($clientId: String, $page: Int, $count: Int){
    GetSAMLIdentityProviderList(clientId: $clientId, page: $page, count: $count){
        totalCount
        list{
            _id
            name
            domain
            image
            appSecret
            appId
            clientId
            description
            isDeleted
            enabled
            when
            SPMetadata
            attributeNameFormat
            customAttributes
            emailDomainTransformation
            authnContextClassRef
            IdPMetadata
            assertionConsumerUrl
            bindings
            nameIds
            attributes
            enableSignRes
            resSignAlgorithm
            resAbstractAlgorithm
            resSignPublicKey
            resSignPrivateKey
            resSignPrivateKeyPass
            enableSignReq
            reqSignPublicKey
            enableEncryptRes
            resEncryptPublicKey
            css
        }
    }
}
''',
    'GetSAMLServiceProviderInfo': '''
query GetSAMLServiceProviderInfo($appId: String!){
    GetSAMLServiceProviderInfo(appId: $appId){
        _id
        name
        domain
        image
        appSecret
        defaultIdPMap{
            _id
            name
            image
            description
            isDeleted
        }
        defaultIdPMapId
        appId
        clientId
        description
        isDeleted
        enabled
        when
        SPMetadata
        IdPMetadata
        IdPEntityID
        assertionConsumeService{
            binding
            url
            isDefault
        }
        mappings{
            username
            nickname
            photo
            company
            providerName
            email
        }
        redirectUrl
        loginUrl
        logoutUrl
        nameId
        enableSignRes
        resSignPublicKey
        hasResEncrypted
        resEncryptAlgorithm
        resAbstractAlgorithm
        resDecryptPrivateKey
        resDecryptPrivateKeyPass
        resEncryptPublicKey
        enableSignReq
        reqSignAlgorithm
        reqAbstractAlgorithm
        reqSignPrivateKey
        reqSignPrivateKeyPass
        reqSignPublicKey
        SPUrl
    }
}
''',
    'GetSAMLServiceProviderList': '''
query GetSAMLServiceProviderList($clientId: String, $page: Int, $count: Int){
    GetSAMLServiceProviderList(clientId: $clientId, page: $page, count: $count){
        totalCount
        list{
            _id
            name
            domain
            image
            appSecret
            defaultIdPMapId
            appId
            clientId
            description
            isDeleted
            enabled
            when
            SPMetadata
            IdPMetadata
            IdPEntityID
            redirectUrl
            loginUrl
            logoutUrl
            nameId
            enableSignRes
            resSignPublicKey
            hasResEncrypted
            resEncryptAlgorithm
            resAbstractAlgorithm
            resDecryptPrivateKey
            resDecryptPrivateKeyPass
            resEncryptPublicKey
            enableSignReq
            reqSignAlgorithm
            reqAbstractAlgorithm
            reqSignPrivateKey
            reqSignPrivateKeyPass
            reqSignPublicKey
            SPUrl
        }
    }
}
''',
    'GetUserAuthorizedApps': '''
query GetUserAuthorizedApps($clientId: String, $userId: String, $page: Int, $count: Int){
    GetUserAuthorizedApps(clientId: $clientId, userId: $userId, page: $page, count: $count){
        totalCount
        OAuthApps{
            _id
            name
            domain
            image
            redirectUris
            appSecret
            client_id
            clientId
            grants
            description
            homepageURL
            isDeleted
            when
            css
            loginUrl
            casExpire
        }
        OIDCApps{
            _id
            name
            domain
            image
            redirect_uris
            client_id
            client_secret
            token_endpoint_auth_method
            id_token_signed_response_alg
            id_token_encrypted_response_alg
            id_token_encrypted_response_enc
            userinfo_signed_response_alg
            userinfo_encrypted_response_alg
            userinfo_encrypted_response_enc
            request_object_signing_alg
            request_object_encryption_alg
            request_object_encryption_enc
            jwks_uri
            _jwks_uri
            custom_jwks
            jwks
            _jwks
            clientId
            grant_types
            response_types
            description
            homepageURL
            isDeleted
            isDefault
            when
            css
            authorization_code_expire
            id_token_expire
            access_token_expire
            cas_expire
            loginUrl
        }
    }
}
''',
    'PreviewEmailByType': '''
query PreviewEmailByType($type: String!, $client: String!, $meta_data: String){
    PreviewEmailByType(type: $type, client: $client, meta_data: $meta_data)
}
''',
    'QueryAppInfoByAppID': '''
query QueryAppInfoByAppID($appId: String, $responseType: String, $redirectUrl: String){
    QueryAppInfoByAppID(appId: $appId, responseType: $responseType, redirectUrl: $redirectUrl){
        _id
        name
        domain
        image
        redirectUris
        appSecret
        client_id
        clientId
        grants
        description
        homepageURL
        isDeleted
        when
        css
        loginUrl
        casExpire
    }
}
''',
    'QueryAppInfoByDomain': '''
query QueryAppInfoByDomain($domain: String){
    QueryAppInfoByDomain(domain: $domain){
        _id
        name
        domain
        image
        redirectUris
        appSecret
        client_id
        clientId
        grants
        description
        homepageURL
        isDeleted
        when
        css
        loginUrl
        casExpire
    }
}
''',
    'QueryClientHasLDAPConfigs': '''
query QueryClientHasLDAPConfigs($clientId: String){
    QueryClientHasLDAPConfigs(clientId: $clientId){
        result
    }
}
''',
    'QueryClientIdByAppId': '''
query QueryClientIdByAppId($appId: String){
    QueryClientIdByAppId(appId: $appId){
        _id
        name
        domain
        image
        redirectUris
        appSecret
        client_id
        clientId
        grants
        description
        homepageURL
        isDeleted
        when
        css
        loginUrl
        casExpire
    }
}
''',
    'QueryDefaultSAMLIdentityProviderSettingsList': '''
query QueryDefaultSAMLIdentityProviderSettingsList($page: Int, $count: Int){
    QueryDefaultSAMLIdentityProviderSettingsList(page: $page, count: $count){
        list{
            _id
            name
            image
            description
            isDeleted
        }
        totalCount
    }
}
''',
    'QueryLDAPServerList': '''
query QueryLDAPServerList($clientId: String!, $page: Int, $count: Int){
    QueryLDAPServerList(clientId: $clientId, page: $page, count: $count){
        list{
            _id
            name
            clientId
            userId
            ldapLink
            baseDN
            searchStandard
            emailPostfix
            username
            password
            description
            enabled
            isDeleted
            createdAt
            updatedAt
        }
        totalCount
    }
}
''',
    'QueryOIDCAppInfoByAppID': '''
query QueryOIDCAppInfoByAppID($appId: String, $responseType: String, $redirectUrl: String){
    QueryOIDCAppInfoByAppID(appId: $appId, responseType: $responseType, redirectUrl: $redirectUrl){
        _id
        name
        domain
        image
        redirect_uris
        client_id
        client_secret
        token_endpoint_auth_method
        id_token_signed_response_alg
        id_token_encrypted_response_alg
        id_token_encrypted_response_enc
        userinfo_signed_response_alg
        userinfo_encrypted_response_alg
        userinfo_encrypted_response_enc
        request_object_signing_alg
        request_object_encryption_alg
        request_object_encryption_enc
        jwks_uri
        _jwks_uri
        custom_jwks
        jwks
        _jwks
        clientId
        grant_types
        response_types
        description
        homepageURL
        isDeleted
        isDefault
        when
        css
        authorization_code_expire
        id_token_expire
        access_token_expire
        cas_expire
        loginUrl
        customStyles{
            forceLogin
            hideQRCode
            hideUP
            hideUsername
            hideRegister
            hidePhone
            hideSocial
            hideClose
            hidePhonePassword
            defaultLoginMethod
        }
    }
}
''',
    'QueryOIDCAppInfoByDomain': '''
query QueryOIDCAppInfoByDomain($domain: String){
    QueryOIDCAppInfoByDomain(domain: $domain){
        _id
        name
        domain
        image
        redirect_uris
        client_id
        client_secret
        token_endpoint_auth_method
        id_token_signed_response_alg
        id_token_encrypted_response_alg
        id_token_encrypted_response_enc
        userinfo_signed_response_alg
        userinfo_encrypted_response_alg
        userinfo_encrypted_response_enc
        request_object_signing_alg
        request_object_encryption_alg
        request_object_encryption_enc
        jwks_uri
        _jwks_uri
        custom_jwks
        jwks
        _jwks
        clientId
        grant_types
        response_types
        description
        homepageURL
        isDeleted
        isDefault
        when
        css
        authorization_code_expire
        id_token_expire
        access_token_expire
        cas_expire
        loginUrl
        customStyles{
            forceLogin
            hideQRCode
            hideUP
            hideUsername
            hideRegister
            hidePhone
            hideSocial
            hideClose
            hidePhonePassword
            defaultLoginMethod
        }
    }
}
''',
    'QuerySAMLIdentityProviderInfoByAppID': '''
query QuerySAMLIdentityProviderInfoByAppID($appId: String){
    QuerySAMLIdentityProviderInfoByAppID(appId: $appId){
        _id
        name
        domain
        image
        appSecret
        appId
        clientId
        description
        isDeleted
        enabled
        when
        SPMetadata
        attributeNameFormat
        customAttributes
        emailDomainTransformation
        authnContextClassRef
        IdPMetadata
        assertionConsumerUrl
        bindings
        nameIds
        attributes
        enableSignRes
        resSignAlgorithm
        resAbstractAlgorithm
        resSignPublicKey
        resSignPrivateKey
        resSignPrivateKeyPass
        enableSignReq
        reqSignPublicKey
        enableEncryptRes
        resEncryptPublicKey
        css
    }
}
''',
    'QuerySAMLIdentityProviderInfoByDomain': '''
query QuerySAMLIdentityProviderInfoByDomain($domain: String){
    QuerySAMLIdentityProviderInfoByDomain(domain: $domain){
        _id
        name
        domain
        image
        appSecret
        appId
        clientId
        description
        isDeleted
        enabled
        when
        SPMetadata
        attributeNameFormat
        customAttributes
        emailDomainTransformation
        authnContextClassRef
        IdPMetadata
        assertionConsumerUrl
        bindings
        nameIds
        attributes
        enableSignRes
        resSignAlgorithm
        resAbstractAlgorithm
        resSignPublicKey
        resSignPrivateKey
        resSignPrivateKeyPass
        enableSignReq
        reqSignPublicKey
        enableEncryptRes
        resEncryptPublicKey
        css
    }
}
''',
    'QuerySAMLServiceProviderInfoByAppID': '''
query QuerySAMLServiceProviderInfoByAppID($appId: String!){
    QuerySAMLServiceProviderInfoByAppID(appId: $appId){
        _id
        name
        domain
        image
        appSecret
        defaultIdPMap{
            _id
            name
            image
            description
            isDeleted
        }
        defaultIdPMapId
        appId
        clientId
        description
        isDeleted
        enabled
        when
        SPMetadata
        IdPMetadata
        IdPEntityID
        assertionConsumeService{
            binding
            url
            isDefault
        }
        mappings{
            username
            nickname
            photo
            company
            providerName
            email
        }
        redirectUrl
        loginUrl
        logoutUrl
        nameId
        enableSignRes
        resSignPublicKey
        hasResEncrypted
        resEncryptAlgorithm
        resAbstractAlgorithm
        resDecryptPrivateKey
        resDecryptPrivateKeyPass
        resEncryptPublicKey
        enableSignReq
        reqSignAlgorithm
        reqAbstractAlgorithm
        reqSignPrivateKey
        reqSignPrivateKeyPass
        reqSignPublicKey
        SPUrl
    }
}
''',
    'QuerySAMLServiceProviderInfoByDomain': '''
query QuerySAMLServiceProviderInfoByDomain($domain: String!){
    QuerySAMLServiceProviderInfoByDomain(domain: $domain){
        _id
        name
        domain
        image
        appSecret
        defaultIdPMap{
            _id
            name
            image
            description
            isDeleted
        }
        defaultIdPMapId
        appId
        clientId
        description
        isDeleted
        enabled
        when
        SPMetadata
        IdPMetadata
        IdPEntityID
        assertionConsumeService{
            binding
            url
            isDefault
        }
        mappings{
            username
            nickname
            photo
            company
            providerName
            email
        }
        redirectUrl
        loginUrl
        logoutUrl
        nameId
        enableSignRes
        resSignPublicKey
        hasResEncrypted
        resEncryptAlgorithm
        resAbstractAlgorithm
        resDecryptPrivateKey
        resDecryptPrivateKeyPass
        resEncryptPublicKey
        enableSignReq
        reqSignAlgorithm
        reqAbstractAlgorithm
        reqSignPrivateKey
        reqSignPrivateKeyPass
        reqSignPublicKey
        SPUrl
    }
}
''',
    'ReadEmailProvider': '''
query ReadEmailProvider($clientId: String){
    ReadEmailProvider(clientId: $clientId){
        _id
        name
        image
        description
        fields{
            label
            type
            placeholder
            help
            value
            options
        }
        client
        user
        status
        provider{
            _id
            name
            image
            description
            client
            user
            status
        }
    }
}
''',
    'ReadEmailProviderByClientAndName': '''
query ReadEmailProviderByClientAndName($clientId: String){
    ReadEmailProviderByClientAndName(clientId: $clientId){
        _id
        user
        client
        status
        fields{
            label
            type
            placeholder
            help
            value
            options
        }
        provider{
            _id
            name
            image
            description
        }
    }
}
''',
    'ReadEmailProviderWithClient': '''
query ReadEmailProviderWithClient{
    ReadEmailProviderWithClient{
        _id
        user
        client
        status
        fields{
            label
            type
            placeholder
            help
            value
            options
        }
        provider{
            _id
            name
            image
            description
        }
    }
}
''',
    'ReadEmailSentList': '''
query ReadEmailSentList($page: Int, $count: Int, $sortBy: String){
    ReadEmailSentList(page: $page, count: $count, sortBy: $sortBy){
        list{
            _id
            subject
            content
            sender
            receivers
            createdAt
        }
        totalCount
    }
}
''',
    'ReadEmailSentListByClient': '''
query ReadEmailSentListByClient($client: String!, $page: Int, $count: Int){
    ReadEmailSentListByClient(client: $client, page: $page, count: $count){
        totalCount
        list{
            _id
            user
            subject
            content
            sender
            receivers
            post
            createdAt
            rejected
            isDeleted
            client
        }
    }
}
''',
    'ReadEmailTemplateByClientAndType': '''
query ReadEmailTemplateByClientAndType($type: String!, $client: String!){
    ReadEmailTemplateByClientAndType(type: $type, client: $client){
        _id
        type
        sender
        object
        hasURL
        URLExpireTime
        status
        redirectTo
        content
    }
}
''',
    'ReadEmailTemplatesByClient': '''
query ReadEmailTemplatesByClient($clientId: String!){
    ReadEmailTemplatesByClient(clientId: $clientId){
        _id
        user
        client
        template{
            _id
            type
            sender
            object
            hasURL
            URLExpireTime
            status
            redirectTo
            content
        }
        type
        sender
        object
        hasURL
        URLExpireTime
        redirectTo
        status
        content
    }
}
''',
    'ReadEmailTemplatesBySystem': '''
query ReadEmailTemplatesBySystem{
    ReadEmailTemplatesBySystem{
        _id
        user
        client
        template{
            _id
            type
            sender
            object
            hasURL
            URLExpireTime
            status
            redirectTo
            content
        }
        type
        sender
        object
        hasURL
        URLExpireTime
        redirectTo
        status
        content
    }
}
''',
    'ReadOauthList': '''
query ReadOauthList($clientId: String, $dontGetURL: Boolean, $useGuard: Boolean){
    ReadOauthList(clientId: $clientId, dontGetURL: $dontGetURL, useGuard: $useGuard){
        _id
        name
        alias
        image
        description
        enabled
        url
        client
        user
        oAuthUrl
        wxappLogo
        fields{
            label
            type
            placeholder
            value
            checked
        }
        oauth{
            _id
            name
            alias
            image
            description
            enabled
            url
            client
            user
            oAuthUrl
            wxappLogo
        }
    }
}
''',
    'ReadOrders': '''
query ReadOrders($user: String, $page: Int, $count: Int){
    ReadOrders(user: $user, page: $page, count: $count){
        list{
            _id
            client
            user
            timeOfPurchase
            flowNumber
            price
            createdAt
            completed
            payMethod
            endAt
        }
        totalCount
    }
}
''',
    'ReadSAMLSPList': '''
query ReadSAMLSPList($clientId: String!){
    ReadSAMLSPList(clientId: $clientId){
        providerName
        url
        logo
    }
}
''',
    'ReadSystemPricing': '''
query ReadSystemPricing{
    ReadSystemPricing{
        _id
        type
        startNumber
        freeNumber
        startPrice
        maxNumber
        d
        features
    }
}
''',
    'ReadUserPricing': '''
query ReadUserPricing($userId: String, $clientId: String){
    ReadUserPricing(userId: $userId, clientId: $clientId){
        user
        client
        isFree
        pricing{
            number
        }
        freeNumber
    }
}
''',
    'TestLDAPServer': '''
query TestLDAPServer($name: String!, $clientId: String!, $userId: String!, $ldapLink: String!, $baseDN: String!, $searchStandard: String!, $username: String!, $password: String!, $emailPostfix: String, $description: String, $enabled: Boolean){
    TestLDAPServer(name: $name, clientId: $clientId, userId: $userId, ldapLink: $ldapLink, baseDN: $baseDN, searchStandard: $searchStandard, username: $username, password: $password, emailPostfix: $emailPostfix, description: $description, enabled: $enabled){
        result
    }
}
''',
    'TestLDAPUser': '''
query TestLDAPUser($testUsername: String!, $testPassword: String!, $name: String!, $clientId: String!, $userId: String!, $ldapLink: String!, $baseDN: String!, $searchStandard: String!, $username: String!, $password: String!, $emailPostfix: String, $description: String, $enabled: Boolean){
    TestLDAPUser(testUsername: $testUsername, testPassword: $testPassword, name: $name, clientId: $clientId, userId: $userId, ldapLink: $ldapLink, baseDN: $baseDN, searchStandard: $searchStandard, username: $username, password: $password, emailPostfix: $emailPostfix, description: $description, enabled: $enabled){
        result
    }
}
''',
    'adConnectorByProvider': '''
query adConnectorByProvider($providerId: String!, $providerType: providerType!){
    adConnectorByProvider(providerId: $providerId, providerType: $providerType){
        _id
        name
        logo
        status
    }
}
''',
    'adConnectorList': '''
query adConnectorList($userPoolId: String!, $providerType: providerType){
    adConnectorList(userPoolId: $userPoolId, providerType: $providerType){
        _id
        name
        secret
        salt
        logo
        enabled
        userPoolId
        status
        createdAt
    }
}
''',
    'bindedOAuthList': '''
query bindedOAuthList($client: String!, $user: String){
    bindedOAuthList(client: $client, user: $user){
        _id
        user
        client
        type
        unionid
        userInfo
        createdAt
    }
}
''',
    'checkAdConnectorStatus': '''
query checkAdConnectorStatus($adConnectorId: String!){
    checkAdConnectorStatus(adConnectorId: $adConnectorId)
}
''',
    'checkIsReservedDomain': '''
query checkIsReservedDomain($domainValue: String!){
    checkIsReservedDomain(domainValue: $domainValue){
        domainValue
        isReserved
    }
}
''',
    'checkLoginStatus': '''
query checkLoginStatus($token: String){
    checkLoginStatus(token: $token){
        message
        code
        status
        token{
            iat
            exp
        }
    }
}
''',
    'checkPhoneCode': '''
query checkPhoneCode($userPoolId: String!, $phone: String!, $phoneCode: String!){
    checkPhoneCode(userPoolId: $userPoolId, phone: $phone, phoneCode: $phoneCode){
        message
        code
        status
    }
}
''',
    'client': '''
query client($id: String!, $userId: String, $fromAdmin: Boolean) {
  client(id: $id, userId: $userId, fromAdmin: $fromAdmin) {
    _id
    user {
      _id
      username
      email
      unionid
      openid
      emailVerified
      phone
      phoneVerified
      nickname
      company
      photo
      browser
      password
      registerInClient
      registerMethod
      oauth
      token
      tokenExpiredAt
      loginsCount
      lastLogin
      lastIP
      signedUp
      blocked
      isDeleted
      device
      name
      givenName
      familyName
      middleName
      profile
      preferredUsername
      website
      gender
      birthdate
      zoneinfo
      locale
      address
      formatted
      streetAddress
      locality
      region
      postalCode
      country
      updatedAt
      oldPassword
      metadata
    }
    clientType {
      _id
      name
      description
      image
      example
    }
    userPoolTypes {
      _id
      name
      description
      image
      example
    }
    usersCount
    logo
    emailVerifiedDefault
    sendWelcomeEmail
    registerDisabled
    showWXMPQRCode
    useMiniLogin
    useSelfWxapp
    allowedOrigins
    name
    secret
    token
    descriptions
    jwtExpired
    createdAt
    isDeleted
    frequentRegisterCheck {
      timeInterval
      limit
      enable
    }
    loginFailCheck {
      timeInterval
      limit
      enable
    }
    enableEmail
    changePhoneStrategy {
      verifyOldPhone
    }
    changeEmailStrategy {
      verifyOldEmail
    }
    qrcodeLoginStrategy {
      qrcodeExpiresAfter
      returnFullUserInfo
      allowExchangeUserInfoFromBrowser
      ticketExpiresAfter
    }
    app2WxappLoginStrategy {
      ticketExpriresAfter
      ticketExchangeUserInfoNeedSecret
    }
  }
}

''',
    'clientRoles': '''
query clientRoles($client: String!, $page: Int, $count: Int){
    clientRoles(client: $client, page: $page, count: $count){
        list{
            _id
            name
            descriptions
            client
            permissions
            createdAt
        }
        totalCount
    }
}
''',
    'decodeJwtToken': '''
query decodeJwtToken($token: String){
    decodeJwtToken(token: $token){
        data{
            email
            id
            clientId
            unionid
        }
        status{
            message
            code
            status
        }
        iat
        exp
    }
}
''',
    'emailDomainTopNList': '''
query emailDomainTopNList($userPoolId: String!){
    emailDomainTopNList(userPoolId: $userPoolId){
        domain
        count
    }
}
''',
    'findClientsByIdArray': '''
query findClientsByIdArray($clientsId: [String]){
    findClientsByIdArray(clientsId: $clientsId){
        list{
            _id
            name
            createdAt
            usersCount
        }
        totalCount
    }
}
''',
    'getAccessTokenByAppSecret': '''
query getAccessTokenByAppSecret(
  $secret: String
  $clientId: String
  $retUserId: Boolean
  $timestamp: String
  $signature: String
  $nonce: Int
) {
  getAccessTokenByAppSecret(
    secret: $secret
    clientId: $clientId
    retUserId: $retUserId
    timestamp: $timestamp
    signature: $signature
    nonce: $nonce
  )
}

''',
    'getAllWebhooks': '''
query getAllWebhooks($client: String!){
    getAllWebhooks(client: $client){
        _id
        client
        events{
            name
            label
            description
        }
        url
        isLastTimeSuccess
        contentType
        secret
        enable
    }
}
''',
    'getAppSecretByClientId': '''
query getAppSecretByClientId($token: String, $clientId: String){
    getAppSecretByClientId(token: $token, clientId: $clientId){
        secret
        clientId
    }
}
''',
    'getClientWhenSdkInit': '''
query getClientWhenSdkInit($secret: String, $clientId: String, $retUserId: Boolean, $timestamp: String, $signature: String, $nonce: Int){
    getClientWhenSdkInit(secret: $secret, clientId: $clientId, retUserId: $retUserId, timestamp: $timestamp, signature: $signature, nonce: $nonce){
        clientInfo{
            _id
            usersCount
            logo
            emailVerifiedDefault
            sendWelcomeEmail
            registerDisabled
            showWXMPQRCode
            useMiniLogin
            useSelfWxapp
            allowedOrigins
            name
            secret
            token
            descriptions
            jwtExpired
            createdAt
            isDeleted
            enableEmail
        }
        accessToken
    }
}
''',
    'getCustomMFA': '''
query getCustomMFA($userIdInMiniLogin: String!, $page: Int, $count: Int){
    getCustomMFA(userIdInMiniLogin: $userIdInMiniLogin, page: $page, count: $count){
        list{
            _id
            userIdInMiniLogin
            remark
            name
            secret
        }
        total
    }
}
''',
    'getOAuthedAppInfo': '''
query getOAuthedAppInfo($appId: String!){
    getOAuthedAppInfo(appId: $appId){
        _id
        name
        domain
        image
        redirectUris
        appSecret
        client_id
        clientId
        grants
        description
        homepageURL
        isDeleted
        when
        css
        loginUrl
        casExpire
    }
}
''',
    'getOAuthedAppList': '''
query getOAuthedAppList($clientId: String, $page: Int, $count: Int){
    getOAuthedAppList(clientId: $clientId, page: $page, count: $count){
        totalCount
        list{
            _id
            name
            domain
            image
            redirectUris
            appSecret
            client_id
            clientId
            grants
            description
            homepageURL
            isDeleted
            when
            css
            loginUrl
            casExpire
        }
    }
}
''',
    'getUserLoginAreaStatisticOfClient': '''
query getUserLoginAreaStatisticOfClient($userPool: String!, $start: String, $end: String){
    getUserLoginAreaStatisticOfClient(userPool: $userPool, start: $start, end: $end)
}
''',
    'getUserPoolSettings': '''
query getUserPoolSettings($userPoolId: String!){
    getUserPoolSettings(userPoolId: $userPoolId){
        _id
        user{
            _id
            username
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            nickname
            company
            photo
            browser
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            device
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            oldPassword
            metadata
        }
        clientType{
            _id
            name
            description
            image
            example
        }
        userPoolTypes{
            _id
            name
            description
            image
            example
        }
        usersCount
        logo
        emailVerifiedDefault
        sendWelcomeEmail
        registerDisabled
        showWXMPQRCode
        useMiniLogin
        useSelfWxapp
        allowedOrigins
        name
        secret
        token
        descriptions
        jwtExpired
        createdAt
        isDeleted
        frequentRegisterCheck{
            timeInterval
            limit
            enable
        }
        loginFailCheck{
            timeInterval
            limit
            enable
        }
        enableEmail
        changePhoneStrategy{
            verifyOldPhone
        }
        changeEmailStrategy{
            verifyOldEmail
        }
        qrcodeLoginStrategy{
            qrcodeExpiresAfter
            returnFullUserInfo
            allowExchangeUserInfoFromBrowser
            ticketExpiresAfter
        }
        app2WxappLoginStrategy{
            ticketExpriresAfter
            ticketExchangeUserInfoNeedSecret
        }
    }
}
''',
    'getWebhookDetail': '''
query getWebhookDetail($client: String!){
    getWebhookDetail(client: $client){
        _id
        client
        events{
            name
            label
            description
        }
        url
        isLastTimeSuccess
        contentType
        secret
        enable
    }
}
''',
    'getWebhookLogDetail': '''
query getWebhookLogDetail($id: String!){
    getWebhookLogDetail(id: $id){
        _id
        webhook
        client
        event
        request{
            headers
            payload
        }
        response{
            headers
            body
            statusCode
        }
        errorMessage
        when
    }
}
''',
    'getWebhookLogs': '''
query getWebhookLogs($webhook: String!){
    getWebhookLogs(webhook: $webhook){
        _id
        webhook
        client
        event
        request{
            headers
            payload
        }
        response{
            headers
            body
            statusCode
        }
        errorMessage
        when
    }
}
''',
    'getWebhookSettingOptions': '''
query getWebhookSettingOptions{
    getWebhookSettingOptions{
        webhookEvents{
            name
            label
            description
        }
        contentTypes{
            name
            label
        }
    }
}
''',
    'interConnections': '''
query interConnections($userPoolId: String!) {
  interConnections(userPoolId: $userPoolId) {
    sourceUserId
    sourceUserPoolId
    targetUserId
    targetUserPoolId
    enabled
    expiresdAt
  }
}

''',
    'isAdConnectorAlive': '''
query isAdConnectorAlive($adConnectorId: String){
    isAdConnectorAlive(adConnectorId: $adConnectorId){
        isAlive
    }
}
''',
    'isAppAuthorizedByUser': '''
query isAppAuthorizedByUser($userId: String, $appId: String){
    isAppAuthorizedByUser(userId: $userId, appId: $appId){
        authorized
    }
}
''',
    'isClientBelongToUser': '''
query isClientBelongToUser($userId: String, $clientId: String, $permissionDescriptors: [PermissionDescriptorsListInputType]){
    isClientBelongToUser(userId: $userId, clientId: $clientId, permissionDescriptors: $permissionDescriptors)
}
''',
    'isClientOfUser': '''
query isClientOfUser($email: String, $password: String, $clientId: String){
    isClientOfUser(email: $email, password: $password, clientId: $clientId)
}
''',
    'isDomainAvaliable': '''
query isDomainAvaliable($domain: String!){
    isDomainAvaliable(domain: $domain)
}
''',
    'isLoginExpired': '''
query isLoginExpired($id: String!){
    isLoginExpired(id: $id)
}
''',
    'isRootNodeOfOrg': '''
query isRootNodeOfOrg($input: IsRootNodeOfOrgInput!){
    isRootNodeOfOrg(input: $input)
}
''',
    'isUserInGroup': '''
query isUserInGroup($groupId: String!, $userId: String!) {
  isUserInGroup(groupId: $groupId, userId: $userId)
}

''',
    'loginBySecret': '''
query loginBySecret($clientId: String, $secret: String) {
  getAccessTokenByAppSecret(clientId: $clientId, secret: $secret)
}

''',
    'loginCount': '''
query loginCount($userId: String, $clientId: String, $month: String){
    loginCount(userId: $userId, clientId: $clientId, month: $month){
        _id
        client
        count
        month
        isError
        totalNumber
    }
}
''',
    'loginHotDotPicData': '''
query loginHotDotPicData($client: String){
    loginHotDotPicData(client: $client){
        list
    }
}
''',
    'notBindOAuthList': '''
query notBindOAuthList($client: String, $user: String){
    notBindOAuthList(client: $client, user: $user){
        type
        oAuthUrl
        image
        name
        binded
    }
}
''',
    'org': '''
query org($_id: String!){
    org(_id: $_id){
        _id
        nodes{
            _id
            name
            description
            createdAt
            updatedAt
            children
            root
        }
    }
}
''',
    'orgChildrenNodes': '''
query orgChildrenNodes($input: OrgChildrenNodesInput!){
    orgChildrenNodes(input: $input){
        group{
            _id
            userPoolId
            name
            description
            createdAt
            updatedAt
        }
        depth
    }
}
''',
    'orgNodeUserList': '''
query orgNodeUserList($orgId: String!, $nodeId: String!, $page: Int, $count: Int, $includeChildrenNodes: Boolean){
    orgNodeUserList(orgId: $orgId, nodeId: $nodeId, page: $page, count: $count, includeChildrenNodes: $includeChildrenNodes){
        list{
            _id
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            username
            nickname
            company
            photo
            browser
            device
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            customData
            metadata
        }
        totalCount
    }
}
''',
    'orgRootNode': '''
query orgRootNode($sortBy: SortByEnum, $page: Int, $count: Int, $_id: String!){
    orgRootNode(_id: $_id){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        roles{
            totalCount
        }
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'orgs': '''
query orgs($userPoolId: String!) {
  orgs(userPoolId: $userPoolId) {
    totalCount
    list {
      _id
      logo
      nodes {
        _id
        name
        description
        createdAt
        updatedAt
        children
        root
      }
    }
  }
}

''',
    'platformUserGrowthTrend': '''
query platformUserGrowthTrend($today: String){
    platformUserGrowthTrend(today: $today){
        day
        count
    }
}
''',
    'previewEmailTemplate': '''
query previewEmailTemplate($type: String, $client: String){
    previewEmailTemplate(type: $type, client: $client){
        message
        code
        status
    }
}
''',
    'providerListByADConnector': '''
query providerListByADConnector($_id: String!){
    providerListByADConnector(_id: $_id){
        providerType
        providerId
        userPoolId
        adConnectorId
    }
}
''',
    'qiNiuUploadToken': '''
query qiNiuUploadToken($type: String){
    qiNiuUploadToken(type: $type)
}
''',
    'qpsByTime': '''
query qpsByTime($startTime: String, $endTime: String, $currentTime: String){
    qpsByTime(startTime: $startTime, endTime: $endTime, currentTime: $currentTime){
        qps
        time
    }
}
''',
    'queryAuthAuditRecords': '''
query queryAuthAuditRecords($userPoolId: String!, $sortBy: String, $page: Int, $count: Int){
    queryAuthAuditRecords(userPoolId: $userPoolId, sortBy: $sortBy, page: $page, count: $count){
        list{
            userPoolId
            appType
            appId
            event
            userId
            createdAt
        }
        totalCount
    }
}
''',
    'queryAuthorizedUserPool': '''
query queryAuthorizedUserPool($unionid: String, $phone: String, $openid: String, $page: Int, $count: Int){
    queryAuthorizedUserPool(unionid: $unionid, phone: $phone, openid: $openid, page: $page, count: $count){
        list{
            userId
        }
        total
    }
}
''',
    'queryClient': '''
query queryClient($id: String!){
    queryClient(id: $id){
        _id
        user{
            _id
            username
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            nickname
            company
            photo
            browser
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            device
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            oldPassword
            metadata
        }
        clientType{
            _id
            name
            description
            image
            example
        }
        userPoolTypes{
            _id
            name
            description
            image
            example
        }
        usersCount
        logo
        emailVerifiedDefault
        sendWelcomeEmail
        registerDisabled
        showWXMPQRCode
        useMiniLogin
        useSelfWxapp
        allowedOrigins
        name
        secret
        token
        descriptions
        jwtExpired
        createdAt
        isDeleted
        frequentRegisterCheck{
            timeInterval
            limit
            enable
        }
        loginFailCheck{
            timeInterval
            limit
            enable
        }
        enableEmail
        changePhoneStrategy{
            verifyOldPhone
        }
        changeEmailStrategy{
            verifyOldEmail
        }
        qrcodeLoginStrategy{
            qrcodeExpiresAfter
            returnFullUserInfo
            allowExchangeUserInfoFromBrowser
            ticketExpiresAfter
        }
        app2WxappLoginStrategy{
            ticketExpriresAfter
            ticketExchangeUserInfoNeedSecret
        }
    }
}
''',
    'queryCollaborationByUserPoolIdAndUserId': '''
query queryCollaborationByUserPoolIdAndUserId($userId: String!, $userPoolId: String!){
    queryCollaborationByUserPoolIdAndUserId(userId: $userId, userPoolId: $userPoolId){
        _id
        createdAt
        owner{
            _id
            username
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            nickname
            company
            photo
            browser
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            device
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            oldPassword
            metadata
        }
        collaborator{
            _id
            username
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            nickname
            company
            photo
            browser
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            device
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            oldPassword
            metadata
        }
        userPool{
            _id
            usersCount
            logo
            emailVerifiedDefault
            sendWelcomeEmail
            registerDisabled
            showWXMPQRCode
            useMiniLogin
            useSelfWxapp
            allowedOrigins
            name
            secret
            token
            descriptions
            jwtExpired
            createdAt
            isDeleted
            enableEmail
        }
        permissionDescriptors{
            permissionId
            name
            operationAllow
        }
    }
}
''',
    'queryCollaborativeUserPoolByUserId': '''
query queryCollaborativeUserPoolByUserId($userId: String!, $page: Int, $count: Int){
    queryCollaborativeUserPoolByUserId(userId: $userId, page: $page, count: $count){
        list{
            _id
            createdAt
        }
        totalCount
    }
}
''',
    'queryCollaboratorPermissions': '''
query queryCollaboratorPermissions($userId: String, $collaborationId: String){
    queryCollaboratorPermissions(userId: $userId, collaborationId: $collaborationId){
        collaborator{
            _id
            username
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            nickname
            company
            photo
            browser
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            device
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            oldPassword
            metadata
        }
        list{
            permissionId
            name
            operationAllow
        }
    }
}
''',
    'queryCollaboratorsByUserPoolId': '''
query queryCollaboratorsByUserPoolId($userPoolId: String!, $count: Int, $page: Int){
    queryCollaboratorsByUserPoolId(userPoolId: $userPoolId, count: $count, page: $page){
        collaborationId
        list{
            _id
            createdAt
        }
    }
}
''',
    'queryInvitation': '''
query queryInvitation($client: String!){
    queryInvitation(client: $client){
        client
        phone
        isDeleted
        createdAt
        updatedAt
    }
}
''',
    'queryInvitationState': '''
query queryInvitationState($client: String!){
    queryInvitationState(client: $client){
        client
        enablePhone
        createdAt
        updatedAt
    }
}
''',
    'queryMFA': '''
query queryMFA($_id: String, $userId: String, $userPoolId: String){
    queryMFA(_id: $_id, userId: $userId, userPoolId: $userPoolId){
        _id
        userId
        userPoolId
        enable
        shareKey
    }
}
''',
    'queryOperationLogs': '''
query queryOperationLogs($userPoolId: String!, $coll: String!, $page: Int, $count: Int){
    queryOperationLogs(userPoolId: $userPoolId, coll: $coll, page: $page, count: $count){
        totalCount
        list{
            operatorId
            operatorName
            operatorAvatar
            isAdmin
            isCollaborator
            isOwner
            operationType
            updatedFields
            removedFields
            operateAt
            fullDocument
            coll
        }
    }
}
''',
    'queryPasswordFaasEnabled': '''
query queryPasswordFaasEnabled($client: String!){
    queryPasswordFaasEnabled(client: $client){
        encryptUrl
        decryptUrl
        user
        client
        logs
        enable
        createdAt
        updatedAt
    }
}
''',
    'queryPasswordStrengthSettingsByUserPoolId': '''
query queryPasswordStrengthSettingsByUserPoolId($userPoolId: String!){
    queryPasswordStrengthSettingsByUserPoolId(userPoolId: $userPoolId){
        userPoolId
        pwdStrength
    }
}
''',
    'queryPermissionList': '''
query queryPermissionList{
    queryPermissionList{
        list{
            _id
            name
            affect
            description
        }
        totalCount
    }
}
''',
    'queryProviderInfoByAppId': '''
query queryProviderInfoByAppId($appId: String){
    queryProviderInfoByAppId(appId: $appId){
        _id
        type
        name
        image
        domain
        clientId
        client_id
        css
        redirect_uris
    }
}
''',
    'queryProviderInfoByDomain': '''
query queryProviderInfoByDomain($domain: String){
    queryProviderInfoByDomain(domain: $domain){
        _id
        type
        name
        image
        domain
        clientId
        client_id
        css
        redirect_uris
    }
}
''',
    'queryRBACGroupUserList': '''
query QueryRBACGroupUserList(
  $_id: String!
  $sortBy: SortByEnum = CREATEDAT_DESC
  $page: Int = 0
  $count: Int = 10
) {
  rbacGroup(_id: $_id) {
    users(sortBy: $sortBy, page: $page, count: $count) {
      totalCount
      list {
        _id
        unionid
        email
        emailVerified
        username
        nickname
        company
        photo
        phone
        browser
        registerInClient
        registerMethod
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        metadata
      }
    }
  }
}

''',
    'queryRoleByUserId': '''
query queryRoleByUserId($user: String!, $client: String!){
    queryRoleByUserId(user: $user, client: $client){
        list{
            _id
            createdAt
        }
        totalCount
    }
}
''',
    'querySMSSendCount': '''
query querySMSSendCount($userPoolId: String!){
    querySMSSendCount(userPoolId: $userPoolId){
        count
        limitCount
    }
}
''',
    'querySystemOAuthSetting': '''
query querySystemOAuthSetting{
    querySystemOAuthSetting{
        _id
        name
        alias
        image
        description
        enabled
        url
        client
        user
        oAuthUrl
        wxappLogo
        fields{
            label
            type
            placeholder
            value
            checked
        }
        oauth{
            _id
            name
            alias
            image
            description
            enabled
            url
            client
            user
            oAuthUrl
            wxappLogo
        }
    }
}
''',
    'queryUserPoolCommonInfo': '''
query queryUserPoolCommonInfo($userPoolId: String!){
    queryUserPoolCommonInfo(userPoolId: $userPoolId){
        _id
        changePhoneStrategy{
            verifyOldPhone
        }
        changeEmailStrategy{
            verifyOldEmail
        }
    }
}
''',
    'rbacGroupList': '''
query rbacGroupList($userPoolId: String!, $sortBy: SortByEnum, $page: Int, $count: Int){
    rbacGroupList(userPoolId: $userPoolId, sortBy: $sortBy, page: $page, count: $count){
        totalCount
        list{
            _id
            userPoolId
            name
            description
            createdAt
            updatedAt
        }
    }
}
''',
    'rbacPermission': '''
query rbacPermission($_id: String!){
    rbacPermission(_id: $_id){
        _id
        name
        userPoolId
        createdAt
        updatedAt
        description
    }
}
''',
    'rbacPermissionList': '''
query rbacPermissionList($userPoolId: String!, $sortBy: SortByEnum, $page: Int, $count: Int){
    rbacPermissionList(userPoolId: $userPoolId, sortBy: $sortBy, page: $page, count: $count){
        totalCount
        list{
            _id
            name
            userPoolId
            createdAt
            updatedAt
            description
        }
    }
}
''',
    'rbacRole': '''
query rbacRole($sortBy: SortByEnum, $page: Int, $count: Int, $_id: String!){
    rbacRole(_id: $_id){
        _id
        userPoolId
        name
        description
        createdAt
        updatedAt
        permissions{
            totalCount
        }
        users(sortBy: $sortBy, page: $page, count: $count){
            totalCount
        }
    }
}
''',
    'rbacRoleList': '''
query rbacRoleList($userPoolId: String!, $sortBy: SortByEnum, $page: Int, $count: Int){
    rbacRoleList(userPoolId: $userPoolId, sortBy: $sortBy, page: $page, count: $count){
        totalCount
        list{
            _id
            userPoolId
            name
            description
            createdAt
            updatedAt
        }
    }
}
''',
    'recentServiceCall': '''
query recentServiceCall($today: String){
    recentServiceCall(today: $today){
        userService{
            day
            count
        }
        emailService{
            day
            count
        }
        oAuthService{
            day
            count
        }
        payService{
            day
            count
        }
    }
}
''',
    'registerEveryDayCount': '''
query registerEveryDayCount($client: String){
    registerEveryDayCount(client: $client){
        list
    }
}
''',
    'registerMethodTopList': '''
query registerMethodTopList($userPoolId: String!){
    registerMethodTopList(userPoolId: $userPoolId){
        method
        count
    }
}
''',
    'requestList': '''
query requestList($page: Int, $count: Int){
    requestList(page: $page, count: $count){
        totalCount
        list{
            _id
            when
            where
            ip
            size
            responseTime
            service
        }
    }
}
''',
    'ruleById': '''
query ruleById($_id: String!){
    ruleById(_id: $_id){
        _id
        userPoolId
        name
        description
        type
        enabled
        faasUrl
        code
        order
        async
        createdAt
        updatedAt
    }
}
''',
    'ruleEnv': '''
query ruleEnv($userPoolId: String!){
    ruleEnv(userPoolId: $userPoolId){
        totalCount
        list{
            key
            value
        }
    }
}
''',
    'rules': '''
query rules($userPoolId: String!){
    rules(userPoolId: $userPoolId){
        totalCount
        list{
            _id
            userPoolId
            name
            description
            type
            enabled
            faasUrl
            code
            order
            async
            createdAt
            updatedAt
        }
    }
}
''',
    'searchOrgNodes': '''
query searchOrgNodes($orgId: String!, $name: String, $metadata: [KeyValuePair!]) {
  searchOrgNodes(orgId: $orgId, name: $name, metadata: $metadata) {
    _id
    name
    description
    createdAt
    updatedAt
  }
}

''',
    'searchUser': '''
query searchUser($type: String!, $value: String!, $registerInClient: String!, $page: Int, $count: Int){
    searchUser(type: $type, value: $value, registerInClient: $registerInClient, page: $page, count: $count){
        list{
            _id
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            username
            nickname
            company
            photo
            browser
            device
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            customData
            metadata
        }
        totalCount
    }
}
''',
    'searchUserBasicInfoById': '''
query searchUserBasicInfoById($userId: String){
    searchUserBasicInfoById(userId: $userId){
        _id
        username
        photo
        email
    }
}
''',
    'statistic': '''
query statistic($sortBy: String, $page: Int, $count: Int){
    statistic(sortBy: $sortBy, page: $page, count: $count){
        list{
            _id
            username
            email
            loginsCount
            appsCount
            OAuthCount
        }
        totalCount
    }
}
''',
    'todayGeoDistribution': '''
query todayGeoDistribution($today: String){
    todayGeoDistribution(today: $today){
        city
        size
        point
    }
}
''',
    'user': '''
query user($id: String, $registerInClient: String, $token: String, $auth: Boolean, $userLoginHistoryPage: Int, $userLoginHistoryCount: Int){
    user(id: $id, registerInClient: $registerInClient, token: $token, auth: $auth, userLoginHistoryPage: $userLoginHistoryPage, userLoginHistoryCount: $userLoginHistoryCount){
        _id
        email
        unionid
        openid
        emailVerified
        phone
        phoneVerified
        username
        nickname
        company
        photo
        browser
        device
        password
        registerInClient
        registerMethod
        oauth
        token
        tokenExpiredAt
        loginsCount
        lastLogin
        lastIP
        signedUp
        blocked
        isDeleted
        name
        givenName
        familyName
        middleName
        profile
        preferredUsername
        website
        gender
        birthdate
        zoneinfo
        locale
        address
        formatted
        streetAddress
        locality
        region
        postalCode
        country
        updatedAt
        metadata
    }
}
''',
    'userAnalytics': '''
query userAnalytics($clientId: String){
    userAnalytics(clientId: $clientId){
        usersAddedToday{
            length
        }
        usersAddedLastWeek{
            length
        }
        usersLoginLastWeek{
            length
        }
        totalUsers{
            length
        }
        allUsers
        totalApps
    }
}
''',
    'userClientList': '''
query userClientList($page: Int, $count: Int, $sortBy: String){
    userClientList(page: $page, count: $count, sortBy: $sortBy){
        list{
            _id
            name
            createdAt
            usersCount
        }
        totalCount
    }
}
''',
    'userClientTypes': '''
query userClientTypes{
    userClientTypes{
        _id
        name
        description
        image
        example
    }
}
''',
    'userClients': '''
query userClients($userId: String!, $page: Int, $count: Int, $computeUsersCount: Boolean){
    userClients(userId: $userId, page: $page, count: $count, computeUsersCount: $computeUsersCount){
        list{
            _id
            usersCount
            logo
            emailVerifiedDefault
            sendWelcomeEmail
            registerDisabled
            showWXMPQRCode
            useMiniLogin
            useSelfWxapp
            allowedOrigins
            name
            secret
            token
            descriptions
            jwtExpired
            createdAt
            isDeleted
            enableEmail
        }
        totalCount
    }
}
''',
    'userExist': '''
query userExist($userPoolId: String!, $email: String, $phone: String, $username: String){
    userExist(userPoolId: $userPoolId, email: $email, phone: $phone, username: $username)
}
''',
    'userGroup': '''
query userGroup($group: String!, $client: String!, $page: Int, $count: Int){
    userGroup(group: $group, client: $client, page: $page, count: $count){
        list{
            _id
            createdAt
        }
        totalCount
    }
}
''',
    'userGroupList': '''
query userGroupList($_id: String!){
    userGroupList(_id: $_id){
        totalCount
        list{
            _id
            userPoolId
            name
            description
            createdAt
            updatedAt
        }
        rawList
    }
}
''',
    'userMetadata': '''
query userMetadata($_id: String!){
    userMetadata(_id: $_id){
        totalCount
        list{
            key
            value
        }
    }
}
''',
    'userOAuthCount': '''
query userOAuthCount($userIds: [String]){
    userOAuthCount(userIds: $userIds)
}
''',
    'userPatch': '''
query userPatch($ids: String){
    userPatch(ids: $ids){
        list{
            _id
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            username
            nickname
            company
            photo
            browser
            device
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            customData
            metadata
        }
        totalCount
    }
}
''',
    'userPermissionList': '''
query userPermissionList($_id: String!){
    userPermissionList(_id: $_id){
        totalCount
        list{
            _id
            name
            userPoolId
            createdAt
            updatedAt
            description
        }
        rawList
    }
}
''',
    'userRoleList': '''
query userRoleList($_id: String!){
    userRoleList(_id: $_id){
        totalCount
        list{
            _id
            userPoolId
            name
            description
            createdAt
            updatedAt
        }
        rawList
    }
}
''',
    'users': '''
query users($registerInClient: String, $page: Int, $count: Int, $populate: Boolean){
    users(registerInClient: $registerInClient, page: $page, count: $count, populate: $populate){
        list{
            _id
            email
            unionid
            openid
            emailVerified
            phone
            phoneVerified
            username
            nickname
            company
            photo
            browser
            device
            password
            registerInClient
            registerMethod
            oauth
            token
            tokenExpiredAt
            loginsCount
            lastLogin
            lastIP
            signedUp
            blocked
            isDeleted
            name
            givenName
            familyName
            middleName
            profile
            preferredUsername
            website
            gender
            birthdate
            zoneinfo
            locale
            address
            formatted
            streetAddress
            locality
            region
            postalCode
            country
            updatedAt
            customData
            metadata
        }
        totalCount
    }
}
''',
    'usersByOidcApp': '''
query usersByOidcApp($userPoolId: String, $page: Int, $count: Int, $appId: String){
    usersByOidcApp(userPoolId: $userPoolId, page: $page, count: $count, appId: $appId){
        list
        totalCount
    }
}
''',
    'usersInGroup': '''
query usersInGroup($group: String, $page: Int, $count: Int){
    usersInGroup(group: $group, page: $page, count: $count){
        list{
            email
            username
            _id
            upgrade
        }
        totalCount
    }
}
''',
    'validatePassword': '''
query validatePassword($userPool: String!, $password: String!, $encryptedPassword: String!){
    validatePassword(userPool: $userPool, password: $password, encryptedPassword: $encryptedPassword){
        isValid
    }
}
''',
    'wxQRCodeLog': '''
query wxQRCodeLog($page: Int, $count: Int, $clientId: String, $sortBy: String){
    wxQRCodeLog(page: $page, count: $count, clientId: $clientId, sortBy: $sortBy){
        list{
            random
            expiredAt
            createdAt
            success
            qrcode
            used
            accessToken
            openid
            userInfo
            redirect
        }
        totalCount
    }
}
'''
}
