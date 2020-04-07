import lxml.etree as ET

REPO_PATH = "wirecard"

# import os
# REPO_PATH = os.path.abspath("wirecard")

GENERIC_XML_FILE = "/credentials_config.xml"
MAGENTO2_XML_FILE = "/config.xml"


def readXmlFiles(xmlFileName):
    return ET.parse(REPO_PATH + xmlFileName)


def readGenericCredentialsConfig():
    genericXmlConfigContent = {}
    for paymentMethod in readXmlFiles(GENERIC_XML_FILE).xpath("//config/payment_methods/*"):
        paymentMethodValues = {}
        for paymentMethodField in list(paymentMethod):
            paymentMethodValues[paymentMethodField.tag] = paymentMethodField.text
        genericXmlConfigContent[paymentMethod.tag] = paymentMethodValues
    return genericXmlConfigContent


def readMagento2CredentialsConfig():
    magento2XmlConfigContent = {}
    for payments in readXmlFiles(MAGENTO2_XML_FILE).getroot().iter('payment'):
        for paymentMethod in payments:
            paymentMethodValues = {}
            for paymentMethodField in paymentMethod:
                paymentMethodValues[paymentMethodField.tag] = paymentMethodField.text
            magento2XmlConfigContent[paymentMethod.tag] = paymentMethodValues
    return magento2XmlConfigContent


def findChangedCredentials(defaultCredentials, magento2Credentials):
    array = []
    naming =  {
         "zapp": "paybybankapp",
         "alipay-xborder": "alipayxborder",
         "ratepay-invoice": "ratepayinvoice",
         "wiretransfer": "poipia"
    }
    for paymentMethodKey, paymentMethodFieldValues in defaultCredentials.items():
        for field in paymentMethodFieldValues.keys():
            for magento2PaymentMethod, magento2PaymentMethodFields in magento2Credentials.items():
                for paymentMethodField in magento2PaymentMethodFields.keys():
                    if naming.get(paymentMethodKey, paymentMethodKey) in magento2PaymentMethod:
                        if field == paymentMethodField and magento2PaymentMethodFields[paymentMethodField] != paymentMethodFieldValues[field]:
                            print(magento2PaymentMethod, magento2PaymentMethodFields[paymentMethodField], " => ",  paymentMethodFieldValues[field])
                            changedCredentialPath = './/' + magento2PaymentMethod + '/' + paymentMethodField
                            array.append([changedCredentialPath, paymentMethodFieldValues[field]])
    return array


def updateMagento2Credentials(credentialsDifference):
    magento2ConfigFile = readXmlFiles(MAGENTO2_XML_FILE)
    for i in range(len(credentialsDifference)):
        magento2ConfigFile.find(credentialsDifference[i][0]).text = credentialsDifference[i][1]
    magento2ConfigFile.write(REPO_PATH + MAGENTO2_XML_FILE,  pretty_print=True, xml_declaration=True, encoding='utf-8')


def updateXmlDeclaration():
    with open(REPO_PATH + MAGENTO2_XML_FILE) as getMagento2XmlContent:
        magento2XmlContent = getMagento2XmlContent.read()
    magento2XmlContent = magento2XmlContent.replace("<?xml version='1.0' encoding='UTF-8'?>", '<?xml version="1.0"?>').replace("-->", "-->\n")

    with open(REPO_PATH + MAGENTO2_XML_FILE, "w") as magento2XmlFile:
        magento2XmlFile.write(magento2XmlContent)


def main():
    defaultCredentials = readGenericCredentialsConfig()
    magento2Credentials = readMagento2CredentialsConfig()
    credentialsDifference = findChangedCredentials(defaultCredentials, magento2Credentials)
    updateMagento2Credentials(credentialsDifference)
    updateXmlDeclaration()


if __name__ == "__main__":
    main()
