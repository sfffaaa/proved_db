module.exports = async promise => {
	try {
		await promise;
	} catch (error) {
		assert.fail('Expected error received, got ${error}');
	}
};
