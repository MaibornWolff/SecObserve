export const validateRuleForm = (values: any) => {
    const errors: any = {};

    if (!values.new_severity && !values.new_status) {
        errors.new_severity = "Either New severity or New status must be set";
        errors.new_status = "Either New severity or New status must be set";
    }

    if (!values.parser && !values.scanner_prefix) {
        errors.parser = "Either Parser or Scanner prefix must be set";
        errors.scanner_prefix = "Either Parser or Scanner prefix must be set";
    }

    return errors;
};
